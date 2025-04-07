# _plugins/mathjax_converter.rb
module Jekyll
    module MathJaxConverter
      def convert_mathjax(input)
        # Replace \[...\] with $$...$$
        output = input.gsub(/\\\[(.*?)\\\]/m, '$$\1$$')
        # Replace \(...\) with $...$
        output.gsub(/\\\((.*?)\\\)/m, '$\1$')
      end
    end
  end
  
  Liquid::Template.register_filter(Jekyll::MathJaxConverter)