class Syntaxhl:

    
    colors = {
            'Token.Text': "#000000",
            'Token.Keyword': "#3060A6",
            'Token.Keyword.Constant': "#3060A6",
            'Token.Keyword.Declaration': "#3060A6",
            'Token.Keyword.Namespace': "#3060A6",
            'Token.Keyword.Pseudo': "#3060A6",
            'Token.Keyword.Reserved': "#3060A6",
            'Token.Keyword.Type': "#3060A6",
            'Token.Name': "#000000",
            'Token.Name.Attribute': "#4E9A06",
            'Token.Name.Builtin': "#4E9A06",
            'Token.Name.Builtin.Pseudo': "#4E9A06",
            'Token.Name.Class': "#4E9A06",
            'Token.Name.Constant': "#4E9A06",
            'Token.Name.Decorator': "#4E9A06",
            'Token.Name.Entity': "#4E9A06",
            'Token.Name.Exception': "#4E9A06",
            'Token.Name.Function': "#4E9A06",
            'Token.Name.Function.Magic': "#4E9A06",
            'Token.Name.Label': "#4E9A06",
            'Token.Name.Namespace': "#4E9A06",
            'Token.Name.Other': "#4E9A06",
            'Token.Name.Tag': "#4E9A06",
            'Token.Name.Variable': "#4E9A06",
            'Token.Name.Variable.Class': "#4E9A06",
            'Token.Name.Variable.Global': "#4E9A06",
            'Token.Name.Variable.Instance': "#4E9A06",
            'Token.Name.Variable.Magic': "#4E9A06",
            'Token.Literal': "#3CBBDD",
            'Token.Literal.Date': "#3CBBDD",
            'Token.Literal.String': "#3CBBDD",
            'Token.Literal.String.Affix': "#3CBBDD",
            'Token.Literal.String.Backtick': "#3CBBDD",
            'Token.Literal.String.Char': "#3CBBDD",
            'Token.Literal.String.Delimiter': "#3CBBDD",
            'Token.Literal.String.Doc': "#3CBBDD",
            'Token.Literal.String.Double': "#3CBBDD",
            'Token.Literal.String.Escape': "#3CBBDD",
            'Token.Literal.String.Heredoc': "#3CBBDD",
            'Token.Literal.String.Interpol': "#3CBBDD",
            'Token.Literal.String.Other': "#3CBBDD",
            'Token.Literal.String.Regex': "#3CBBDD",
            'Token.Literal.String.Single': "#3CBBDD",
            'Token.Literal.String.Symbol': "#3CBBDD",
            'Token.Operator': "#C10E18",
            'Token.Operator.Word': "#C10E18",
            'Token.Punctuation': "#494141",
            'Token.Comment': "#AD7FA8",
            'Token.Comment.Hashbang': "#AD7FA8",
            'Token.Comment.Multiline': "#AD7FA8",
            'Token.Comment.Preproc': "#AD7FA8",
            'Token.Comment.Single': "#AD7FA8",
            'Token.Comment.Special': "#AD7FA8",
            'Token.Literal.Number': "#04137A",
            'Token.Literal.Number.Bin': "#04137A",
            'Token.Literal.Number.Float': "#04137A",
            'Token.Literal.Number.Hex': "#04137A",
            'Token.Literal.Number.Integer': "#04137A",
            'Token.Literal.Number.Integer.Long': "#04137A",
            'Token.Literal.Number.Oct': "#04137A",
            'Token.Declaration': "#F53200",
    }
    
    lexers = {
    'css': pygments.lexers.CssLexer(),
    'html': pygments.lexers.HtmlLexer(),
    'javascript': pygments.lexers.JavascriptLexer(),
    'json': pygments.lexers.JsonLexer(),
    'python3': pygments.lexers.Python3Lexer(),
    'php': pygments.lexers.PhpLexer(startinline=True),
    'mysql': pygments.lexers.MySqlLexer(),
    'sql': pygments.lexers.SqlLexer(),
    'XML': pygments.lexers.XmlLexer()
    }

    def extract_text(event=None, return_mode=False, open_mode=False):
        
        if open_mode is False:

            if return_mode is False:
                
                linestart = textPad.index('insert linestart')
                lineend = textPad.index('insert lineend')
                text = textPad.get(linestart, lineend)
                Syntaxhl.find_syntax(text, linestart, lineend)

            else:
                
                linestart = str(int(textPad.index('insert linestart').split('.')[0]) - 1) + '.' + textPad.index('insert linestart').split('.')[1]
                lineend = str(int(textPad.index('insert lineend').split('.')[0]) - 1) + '.' + textPad.index('insert lineend-1c').split('.')[1]
                text = textPad.get(linestart, lineend)
                Syntaxhl.find_syntax(text, linestart, lineend)
        else:
            text = textPad.get('1.0', 'end')

            for tag in textPad.tag_names():
                
                textPad.tag_remove(tag, '1.0', 'end')
                lines = text.split('\n')
                
            for i in range(len(lines)):
                linestart = f'{str(i + 1)}.0'
                lineend = f'{str(i + 1)}.{len(lines[i])}'
                text = textPad.get(linestart, lineend)
                Syntaxhl.find_syntax(text, linestart, lineend)
        for wordtype in Syntaxhl.colors.keys():
            textPad.tag_config(wordtype, foreground=Syntaxhl.colors[wordtype])



    def find_syntax(text, linestart, lineend):
        count = 0
        lexer = Syntaxhl.lexers[language.get()]
        for tag in textPad.tag_names():  
            textPad.tag_remove(tag, linestart, lineend)
        for pair in pygments.lex(text, lexer):

            wordtype = str(pair[0])
            word = pair[1]
            if word == "\n":
                return
            

            chars = len(word)
            count += chars
            column = int(linestart.split('.')[1])
            line = int(linestart.split('.')[0])
            index = f'{line}.{count}'
            column = int(index.split('.')[1])
            textPad.tag_add(wordtype, f'{line}.{str(column - chars)}', index)
