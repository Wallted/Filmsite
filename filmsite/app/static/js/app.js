$(document).ready(function () {
    var title = $('#opinionTitle')
    title.text("Oceń film")


    function setTitle(value) {
        switch (value) {
            case '1':
                title.text("\"Nieporozumienie\"")
                break
            case '2':
                title.text("\"Bardzo zły\"")
                break
            case '3':
                title.text("\"Słaby\"")
                break
            case '4':
                title.text("\"Ujdzie\"")
                break
            case '5':
                title.text("\"Średni\"")
                break
            case '6':
                title.text("\"Niezły\"")
                break
            case '7':
                title.text("\"Dobry\"")
                break
            case '8':
                title.text("\"Bardzo dobry\"")
                break
            case '9':
                title.text("\"Rewelacyjny\"")
                break
            case '10':
                title.text("\"Arcydzieło\"")
                break
        }
    }

    $("input[type='radio']").click(function () {
        setTitle(this.value)
    });
    
    $("input[type='radio']").each(function (){
        if (this.checked) {
            setTitle(this.value)
        }
    })
});