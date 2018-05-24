$(document).ready(function() {
    createLegend();
    $(document).on("click", ".wordinput .tag", function() {
        $('#wordinput').tagsinput('remove', {word: $(this).text()});
    });

    $(document).on("click", ".animeinput .tag", function() {
        console.log($(this).text());
        $('#animeinput').tagsinput('remove', {anime_english_title: $(this).text()});
    });
    
    // Stop Format on 
    $("#submit").click(function() {
        $('#myform').submit();
    });

    // Anime Search
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

function createLegend() { 
    console.log(anime_scores.data.datasets[0]);
    document.getElementById('chart-legends').innerHTML = anime_scores.generateLegend();
};

function initializeWordSearch(wordList) {
    var word = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('word'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: {
            url: '/static/data/words.json',
            cache: false
        }
    });
    word.initialize();
    $('#wordinput').tagsinput({
        itemValue: 'word',
        typeaheadjs: {
            // name: 'anime_search',
            // image: 'anime_image_url',
            displayKey: 'word',
//            valueKey: 'word',
            // engine: Handlebars,
            // suggestion: ,
            source: word.ttAdapter(),
            hint: true,
            minLength: 3
        },
        confirmKeys: [13, 44, 188],
        maxTags: 5,
        freeInput: false,
        delimiter: '|'
    });
    console.log(wordList);

    for (var word in wordList) {
        $('#wordinput').tagsinput('add', {word: wordList[word]});
    ;}
};

function initializeAnimeSearch(animeList) {
    var anime = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('anime_english_title'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: {
            url: '/static/data/anime_search.json',
            cache: false
        }
    });
    anime.initialize();
    $('#animeinput').tagsinput({
        delimiter: '|',
        itemValue: 'anime_english_title',
        typeaheadjs: {
            displayKey: 'anime_english_title',
            templates: {
                suggestion: function (data) {
                    return '<div class="d-flex">' +
                               '<img class="align-self-center mr-3" src="' + data.anime_image_url + '" alt="Generic placeholder image">' +
                               '<div class="align-self-center">' +
                                   '<div class="d-flex">' +
                                      '<span class="align-self-center search-anime-title">' + data.anime_english_title + '</span>' + 
                                      '<span class="align-self-center search-anime-type">(' + data.anime_type + ')</span>' + 
                                   '</div>' + 
                                   '<p class="search-anime-type">' + data.anime_type + '</p>' + 
                                   '<p class="search-anime-aired">Aired: ' + data.anime_aired + '</p>' + 
                               '</div>' +
                           '</div>'
                }
            },
            source: anime.ttAdapter(),
            hint: true,
            minLength: 3,
        },
        confirmKeys: [13, 44, 188],
        maxTags: 5,
        freeInput: false,
    });
    console.log(animeList);

    for (var anime in animeList) {
        $('#animeinput').tagsinput('add', {anime_english_title: animeList[anime]});
    ;}
};
