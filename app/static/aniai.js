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
        itemValue: 'anime_id',
        itemText: 'anime_english_title',
        typeaheadjs: {
            // name: 'anime_search',
            // image: 'anime_image_url',
            displayKey: 'anime_english_title',
            // valueKey: 'anime_english_title',
            // engine: Handlebars,
            templates: {
                suggestion: function (data) {
                    return '<div><p>' + '<img style="height:50px; width:30px;" src=' + data.anime_image_url + '> ' + data.anime_english_title + '</p></div>';
                }
            },
            // suggestion: ,
            source: anime.ttAdapter(),
            hint: true,
            minLength: 3
        },
        confirmKeys: [13, 44, 188],
        maxTags: 5,
        freeInput: false,
        delimiter: '|'
    });

    // $('#animeinput .typeahead').typeahead({

    // })

    // $('#furtherfilters').click(function() {
    // 	if ($('#furtherfilters').text() == "Show Additional Filters") {
    // 		$('#furtherfilters').text("Hide Additional Filters");
    // 	} else {
    // 		$('#furtherfilters').text("Show Additional Filters");
    // 	};
    // });

    var word = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('word'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: {
            url: '/static/data/words.json'
        }
    });
    word.initialize();
    $('#wordinput').tagsinput({
        typeaheadjs: {
            // name: 'anime_search',
            // image: 'anime_image_url',
            displayKey: 'word',
            valueKey: 'word',
            // engine: Handlebars,
            // suggestion: ,
            source: word.ttAdapter(),
            hint: false,
            minLength: 3
        },
        confirmKeys: [13, 44, 188],
        maxTags: 5,
        freeInput: false,
        delimiter: '|'
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