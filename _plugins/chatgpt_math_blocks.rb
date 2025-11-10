# frozen_string_literal: true

module NumericJungle
  module ChatGPTMathBlocks
    BLOCK_PATTERN = /
      ^([ \t]*)\[\s*\r?\n  # opening bracket, keep indentation
      (.*?)                # block body
      ^\1\]\s*(\r?\n|\z)   # closing bracket that matches indentation
    /mx.freeze

    def self.convert(content)
      content = convert_blocks(content)
      convert_inline_parentheses(content)
    end

    def self.convert_blocks(content)
      content.gsub(BLOCK_PATTERN) do
        match = Regexp.last_match
        indent = match[1] || ''
        body = match[2]
        trailing_newline = match[3] || ''
        next match[0] unless looks_like_math?(body)

        cleaned = sanitize_math_tokens(body.strip)
        prefix = indent.empty? ? "\n" : "\n#{indent}"
        "#{prefix}$$\n#{cleaned}\n#{indent}$$#{trailing_spacing(trailing_newline)}"
      end
    end

    def self.convert_inline_parentheses(content)
      result = +''
      i = 0
      length = content.length
      inline_dollar = false
      display_dollar = false
      display_bracket = false
      inline_command = 0

      while i < length
        if content[i, 2] == '$$'
          display_dollar = !display_dollar
          result << '$$'
          i += 2
          next
        end

        char = content[i]
        if char == '$' && (i.zero? || content[i - 1] != '\\')
          inline_dollar = !inline_dollar unless display_dollar
          result << '$'
          i += 1
          next
        end

        if char == '\\'
          next_char = content[i + 1]
          if next_char
            case next_char
            when '['
              display_bracket = true
            when ']'
              display_bracket = false
            when '('
              inline_command += 1
            when ')'
              inline_command = [inline_command - 1, 0].max
            end
            result << char << next_char
            i += 2
            next
          else
            result << char
            i += 1
            next
          end
        end

        if char == '(' && !within_math?(inline_dollar, display_dollar, display_bracket, inline_command) &&
           inline_candidate_start?(content, i)
          closing_index, body, contains_newline = find_matching_parenthesis(content, i + 1)
          if closing_index && !contains_newline
            stripped = body.strip
            if inline_math_candidate?(stripped)
              sanitized = sanitize_inline_math(stripped)
              result << "$#{sanitized}$"
              i = closing_index + 1
              next
            end
          end
        end

        result << char
        i += 1
      end

      result
    end

    def self.within_math?(inline_dollar, display_dollar, display_bracket, inline_command)
      inline_dollar || display_dollar || display_bracket || inline_command.positive?
    end

    def self.inline_candidate_start?(content, index)
      prev = index.zero? ? "\n" : content[index - 1]
      !prev.match?(/[[:alnum:]_$]/)
    end

    def self.find_matching_parenthesis(content, start_index)
      depth = 1
      i = start_index
      contains_newline = false

      while i < content.length
        char = content[i]
        contains_newline ||= char == "\n"

        if char == '('
          depth += 1
        elsif char == ')'
          depth -= 1
          if depth.zero?
            inner = content[start_index...i]
            return [i, inner, contains_newline]
          end
        end

        i += 1
      end

      [nil, nil, contains_newline]
    end

    def self.inline_math_candidate?(text)
      return false if text.empty?
      return false if text.include?('$$') || text.include?('\\(') || text.include?('\\)') || text.include?('$')
      looks_like_math?(text)
    end

    def self.sanitize_inline_math(text)
      sanitize_math_tokens(text, inline: true)
    end

    def self.sanitize_math_tokens(text, inline: false)
      sanitized = text.dup
      sanitized = sanitized.gsub('|', '&#124;') if inline && sanitized.include?('|')
      if sanitized.include?('*{')
        sanitized = sanitized.gsub('*{', '_{')
      end
      if sanitized.include?('*')
        sanitized = sanitized.gsub(/(?<=\}|[[:alnum:]])\*([[:alnum:]])/, '_\1')
        sanitized = sanitized.gsub(/(?<=\}|[[:alnum:]])\*(\\[A-Za-z]+)/) do
          "_{#{Regexp.last_match(1)}}"
        end
      end
      if sanitized.include?('<')
        sanitized = sanitized.gsub(/(?<!\\)</, '\\lt ')
      end
      if sanitized.include?('>')
        sanitized = sanitized.gsub(/(?<!\\)>/, '\\gt ')
      end
      sanitized
    end

    def self.trailing_spacing(original_newline)
      original_newline == '' ? "\n\n" : "#{original_newline}\n"
    end

    def self.looks_like_math?(text)
      stripped = text.strip
      return false if stripped.empty?

      stripped.include?('\\') || stripped.match?(/[_^=]/)
    end
  end
end

%i[documents pages posts].each do |entity|
  Jekyll::Hooks.register entity, :pre_render do |doc|
    next unless doc.is_a?(Jekyll::Document) || doc.is_a?(Jekyll::Page)

    doc.content = NumericJungle::ChatGPTMathBlocks.convert(doc.content)
  end
end
