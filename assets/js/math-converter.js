(function() {
  const sourceEl = document.getElementById('converter-source');
  const outputEl = document.getElementById('converter-output');
  const previewEl = document.getElementById('converter-preview');
  const convertBtn = document.getElementById('convert-btn');
  const copyBtn = document.getElementById('copy-btn');
  const statusEl = document.getElementById('converter-status');
  const rendererEl = document.getElementById('renderer-base');

  if (!sourceEl || !outputEl || !previewEl || !convertBtn || !copyBtn || !statusEl || !rendererEl) {
    return;
  }

  const CODE_PLACEHOLDER = /@@CODEBLOCK_(\d+)@@/g;
  let tokenId = 0;
  const tokenMap = new Map();

  function nextToken() {
    const token = `@@MATH_IMG_${tokenId}@@`;
    tokenId += 1;
    return token;
  }

  function sanitizeMathTokens(raw, inline) {
    if (!raw) return '';
    let text = raw;
    if (inline && text.includes('|')) {
      text = text.replace(/\|/g, '\\mid ');
    }
    if (text.includes('*{')) {
      text = text.replace(/\*\{/g, '_{');
    }
    text = text.replace(/([0-9A-Za-z}])\*([0-9A-Za-z])/g, '$1_$2');
    text = text.replace(/([0-9A-Za-z}])\*(\\[A-Za-z]+)/g, '$1_{$2}');
    text = text.replace(/!=!/g, '=').replace(/!\+!/g, '+').replace(/!-!/g, '-');
    text = text.replace(/!\\mid!/g, '\\mid ').replace(/!\\mid/g, '\\mid ').replace(/\\mid!/g, '\\mid ');
    text = text.replace(/!\\([A-Za-z]+)/g, '\\$1');
    text = text.replace(/!\(/g, '(').replace(/!\)/g, ')');
    text = text.replace(/\\mid(?=[0-9A-Za-z_\\])/g, '\\mid ');
    text = text.replace(/!\s+/g, ' ');
    let builder = '';
    for (let i = 0; i < text.length; i += 1) {
      const ch = text[i];
      if (ch === '<') {
        builder += (i > 0 && text[i - 1] === '\\') ? ch : '\\lt ';
      } else if (ch === '>') {
        builder += (i > 0 && text[i - 1] === '\\') ? ch : '\\gt ';
      } else {
        builder += ch;
      }
    }
    return builder.trim();
  }

  function encodeFormula(expr, baseUrl, inline) {
    const sanitized = sanitizeMathTokens(expr, inline);
    if (!sanitized) {
      return { replacement: expr, converted: false };
    }
    const encoded = encodeURIComponent(sanitized);
    const url = `${baseUrl}${encoded}`;
    const token = nextToken();
    const html = inline
      ? `<img src="${url}" alt="${sanitized}" class="math-img-inline">`
      : `<div class="math-img-block"><img src="${url}" alt="${sanitized}"></div>`;
    tokenMap.set(token, html);
    return { replacement: token, converted: true };
  }

  function replaceBlocks(text, regex, baseUrl, counters) {
    return text.replace(regex, function(match, expr) {
      const { replacement, converted } = encodeFormula(expr, baseUrl, false);
      if (!converted) {
        return match;
      }
      counters.blocks += 1;
      return `\n${replacement}\n`;
    });
  }

  function replaceInline(text, regex, baseUrl, counters) {
    return text.replace(regex, function(match, expr) {
      const { replacement, converted } = encodeFormula(expr, baseUrl, true);
      if (!converted) {
        return match;
      }
      counters.inline += 1;
      return replacement;
    });
  }

  function convertParenInline(text, baseUrl, counters) {
    let i = 0;
    const length = text.length;
    let result = '';
    let inlineDollar = false;
    let displayDollar = false;
    let displayBracket = false;
    let inlineCommand = 0;

    while (i < length) {
      if (text.startsWith('$$', i)) {
        displayDollar = !displayDollar;
        result += '$$';
        i += 2;
        continue;
      }

      const char = text[i];
      const prevChar = i === 0 ? '' : text[i - 1];

      if (char === '$' && prevChar !== '\\') {
        if (!displayDollar) {
          inlineDollar = !inlineDollar;
        }
        result += '$';
        i += 1;
        continue;
      }

      if (char === '\\') {
        const nextChar = text[i + 1];
        if (nextChar === '[') {
          displayBracket = true;
        } else if (nextChar === ']') {
          displayBracket = false;
        } else if (nextChar === '(') {
          inlineCommand += 1;
        } else if (nextChar === ')') {
          inlineCommand = Math.max(0, inlineCommand - 1);
        }
        result += char;
        if (nextChar) {
          result += nextChar;
          i += 2;
        } else {
          i += 1;
        }
        continue;
      }

      if (char === '(' && !inlineDollar && !displayDollar && !displayBracket && inlineCommand === 0) {
        const prev = i === 0 ? '\n' : text[i - 1];
        if (!/[\w$]/.test(prev)) {
          let depth = 1;
          let k = i + 1;
          let containsNewline = false;
          while (k < length && depth > 0) {
            const current = text[k];
            if (current === '\n') {
              containsNewline = true;
            } else if (current === '(') {
              depth += 1;
            } else if (current === ')') {
              depth -= 1;
            }
            k += 1;
          }
          if (depth === 0 && !containsNewline) {
            const inner = text.slice(i + 1, k - 1).trim();
            if (/[\\_^]/.test(inner) && !inner.includes('![')) {
              const { replacement, converted } = encodeFormula(inner, baseUrl, true);
              if (converted) {
                counters.inline += 1;
                result += `(${replacement})`;
                i = k;
                continue;
              }
            }
          }
        }
      }

      result += char;
      i += 1;
    }
    return result;
  }

  function protectCodeBlocks(text) {
    const blocks = [];
    const safe = text.replace(/```[\s\S]*?```/g, function(block) {
      const token = `@@CODEBLOCK_${blocks.length}@@`;
      blocks.push(block);
      return token;
    });
    return { safe, blocks };
  }

  function restoreCodeBlocks(text, blocks) {
    return text.replace(CODE_PLACEHOLDER, function(_, index) {
      return blocks[Number(index)] || '';
    });
  }

  function escapeHtml(text) {
    return text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  function textChunkToHtml(chunk) {
    if (!chunk) return '';
    const paragraphs = chunk.split(/\n{2,}/);
    return paragraphs.map(paragraph => {
      const escaped = escapeHtml(paragraph).replace(/\n/g, '<br>');
      return `<p>${escaped}</p>`;
    }).join('');
  }

  function assembleHtml(text) {
    const tokenRegex = /@@MATH_IMG_\d+@@/g;
    let match;
    let lastIndex = 0;
    let html = '';

    while ((match = tokenRegex.exec(text)) !== null) {
      const segment = text.slice(lastIndex, match.index);
      if (segment) {
        html += textChunkToHtml(segment);
      }
      const token = match[0];
      html += tokenMap.get(token) || '';
      lastIndex = match.index + token.length;
    }

    const tail = text.slice(lastIndex);
    if (tail) {
      html += textChunkToHtml(tail);
    }

    return html || '<p></p>';
  }

  function convertMarkdown(raw) {
    tokenMap.clear();
    tokenId = 0;
    const baseUrl = rendererEl.value.trim() || 'https://latex.codecogs.com/png.image?';
    const counters = { inline: 0, blocks: 0 };
    const { safe, blocks } = protectCodeBlocks(raw);
    let working = safe;

    working = replaceBlocks(working, /\$\$([\s\S]*?)\$\$/g, baseUrl, counters);
    working = replaceBlocks(working, /\\\[([\s\S]*?)\\\]/g, baseUrl, counters);
    working = working.replace(/(\n|^)\[\s*\n([\s\S]*?)\n\]\s*(?=\n|$)/g, function(match, prefix, expr) {
      const { replacement, converted } = encodeFormula(expr, baseUrl, false);
      if (!converted) {
        return match;
      }
      counters.blocks += 1;
      return `${prefix}${replacement}\n`;
    });
    working = replaceInline(working, /\\\((.+?)\\\)/g, baseUrl, counters);
    working = convertParenInline(working, baseUrl, counters);

    const restored = restoreCodeBlocks(working, blocks);
    const finalHtml = assembleHtml(restored);

    return { html: finalHtml, counters };
  }

  let lastHtmlOutput = '';
  let lastPlainOutput = '';

  convertBtn.addEventListener('click', function() {
    const source = sourceEl.value;
    if (!source.trim()) {
      outputEl.value = '';
      previewEl.innerHTML = '';
      lastHtmlOutput = '';
      lastPlainOutput = '';
      copyBtn.disabled = true;
      statusEl.textContent = 'Paste something to convert.';
      return;
    }
    const { html, counters } = convertMarkdown(source);
    outputEl.value = html;
    previewEl.innerHTML = html;
    lastHtmlOutput = html;
    lastPlainOutput = previewEl.textContent || '';
    copyBtn.disabled = false;
    const total = counters.blocks + counters.inline;
    statusEl.textContent = total
      ? `Converted ${total} formula${total === 1 ? '' : 's'} (${counters.blocks} block, ${counters.inline} inline).`
      : 'No formulas detected — double-check your delimiters.';
  });

  copyBtn.addEventListener('click', async function() {
    if (!lastHtmlOutput) {
      statusEl.textContent = 'Nothing to copy yet.';
      return;
    }
    try {
      if (navigator.clipboard && window.ClipboardItem) {
        const htmlBlob = new Blob([lastHtmlOutput], { type: 'text/html' });
        const textBlob = new Blob([lastPlainOutput], { type: 'text/plain' });
        await navigator.clipboard.write([
          new ClipboardItem({
            'text/html': htmlBlob,
            'text/plain': textBlob
          })
        ]);
      } else {
        await navigator.clipboard.writeText(lastPlainOutput);
      }
      statusEl.textContent = 'Preview content copied. Paste into Google Docs / OneNote.';
    } catch (err) {
      statusEl.textContent = 'Clipboard unavailable — select and copy manually.';
    }
  });
})();
