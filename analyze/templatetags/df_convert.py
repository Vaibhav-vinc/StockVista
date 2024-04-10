from django import template

register = template.Library()


@register.filter(name="getTableHeaderRowFromDF")
def getTableHeaderRowFromDF(df):
    html = "<tr>"
    for col in df.columns:
        html += f'<th scope="col">{col}</th>'
    html += "</tr>"
    return html


@register.filter(name="getTableBodyRowsFromDF")
def getTableBodyRowsFromDF(df):
    html = ""
    for row in df.values:
        row_html = "<tr>\n"
        attr = 'scope="row"'
        tag = "th"
        for value in row:
            row_html += f"\t<{tag} {attr}>{value if type(value)==str else round(value, 3)}</{tag}>\n"
            attr = ""
            tag = "td"
        row_html += "</tr>\n"
        html += row_html
    return html
