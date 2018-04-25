$(document).ready(function() {
    
    // Stop Format on 
    $("#submit").click(function() {
        $('#myform').submit();
    });

    // Anime Search
    var anime = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('anime_english_title'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: {
            url: '/static/data/anime_info.json'
        }
    });
    anime.initialize();
    $('#animeinput').tagsinput({
        typeaheadjs: {
            name: 'anime_info',
            displayKey: 'anime_english_title',
            valueKey: 'anime_english_title',
            source: anime.ttAdapter(),
            hint: true,
            highlight: true,
            minLength: 3
        },
        confirmKeys: [13, 44, 188],
        maxTags: 5,
        freeInput: false,
        delimiter: ','
    });

    // var genre = new Bloodhound({
    //     datumTokenizer: Bloodhound.tokenizers.obj.whitespace('anime_english_title'),
    //     queryTokenizer: Bloodhound.tokenizers.whitespace,
    //     prefetch: {
    //         url: '/static/data/anime_info.json'
    //     }
    // });
    // anime.initialize();
    // $('input').tagsinput({
    //     typeaheadjs: {
    //         name: 'anime_info',
    //         displayKey: 'anime_english_title',
    //         valueKey: 'anime_english_title',
    //         source: anime.ttAdapter(),
    //         hint: true,
    //         // highlight: true
    //         minLength: 3
    //     },
    //     confirmKeys: [13, 44, 188],
    //     maxTags: 5,
    //     freeInput: false,
    //     delimiter: ','
    // });
});