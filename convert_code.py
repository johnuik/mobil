#!/usr/bin/env python3
"""
Convert code snippets in <p> tags to <div class="code-block"> format
This script identifies code patterns and converts them to styled code blocks
"""

import re
from pathlib import Path

# Read the HTML file
html_file = Path('/home/kali/Documents/doc/index.html')
content = html_file.read_text(encoding='utf-8')

# Patterns that indicate code snippets
code_patterns = [
    r'<p>(adb\s+[\w\s<>&;\-\.\/"\']+)</p>',  # adb commands
    r'<p>(frida\s+[\w\s<>&;\-\./"\']+)</p>',  # frida commands
    r'<p>(clutch\s+[\w\s<>&;\-\./"\']+)</p>',  # clutch commands
    r'<p>(cy#\s+[\w\s<>&;\[\]\-\./"\'()\{\}]+)</p>',  # cycript commands
    r'<p>(objection\s+[\w\s<>&;\-\./"\']+)</p>',  # objection commands
    r'<p>(mitmproxy\s+[\w\s<>&;\-\./"\']+)</p>',  # mitmproxy commands
    r'<p>(const-string[\w\s<>&;\-\./"\']+)</p>',  # Smali code
    r'<p>(invoke-[\w\s<>&;\-\./"\'();\{\}]+)</p>',  # Smali instructions
    r'<p>(ps\s+aux[\w\s<>&;\-\./"\'|]+)</p>',  # Shell commands
    r'<p>(expr\s+[\w\s<>&;\-\./"\'=]+)</p>',  # LLDB commands
]

def convert_to_code_block(match):
    """Convert a code match to a code block div"""
    code_content = match.group(1)
    
    # Determine language
    language = 'code'
    if code_content.startswith('adb'):
        language = 'bash'
    elif code_content.startswith('frida') or code_content.startswith('objection'):
        language = 'bash'
    elif code_content.startswith('cy#'):
        language = 'javascript'
    elif code_content.startswith('const-string') or code_content.startswith('invoke-'):
        language = 'smali'
    elif code_content.startswith(('ps ', 'expr')):
        language = 'bash'
    else:
        language = 'plaintext'
    
    # Escape HTML entities in the code
    code_content = code_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    code_block = f'''<div class="code-block">
    <div class="code-block-header">
        <span class="code-block-language">{language}</span>
        <button class="code-block-copy-btn">Copy</button>
    </div>
    <div class="code-block-content"><code>{code_content}</code></div>
</div>'''
    
    return code_block

# Apply conversions for each pattern
for pattern in code_patterns:
    content = re.sub(pattern, convert_to_code_block, content, flags=re.IGNORECASE | re.MULTILINE)

# Write back
html_file.write_text(content, encoding='utf-8')
print("✓ Code blocks conversion complete!")
