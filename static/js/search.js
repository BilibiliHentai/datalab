const log = console.log.bind(console)
$(function(){
    $("#search").click(() => {
        let x = $('#search-bar')
        x.find("input").eq(0).focus()
        if (x.css("display") === "none") {
            x.css("display", "block")
            x.find("input").eq(1).focus()
        } else {
            x.css("display", "none")
        }
    })

    $("#search-bar").keypress(function(e) {
        if(e.which == 13) {
            form = $(this).find("form").eq(0)
            form.submit()
        }     
    });
})