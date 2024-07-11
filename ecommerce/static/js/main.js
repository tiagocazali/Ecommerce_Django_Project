var url = new URL(document.URL);
var itens = document.getElementsByClassName("filter-orderby");

for (i=0; i<itens.length; i++){
    url.searchParams.set("order", itens[i].name);
    itens[i].href = url.href
}