
$(window).load(function(){
    // Instantiate the Bloodhound suggestion engine
    var movies = new Bloodhound({
        datumTokenizer: function (datum) {
            return Bloodhound.tokenizers.whitespace(datum.value);
        },
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
            url: 'http://api.themoviedb.org/3/search/movie?query=%QUERY&api_key=470fd2ec8853e25d2f8d86f685d2270e',
            filter: function (movies) {
                return $.map(movies.results, function (movie) {
                    return {
                        value: movie.original_title,
                        release_date: movie.release_date,
                        poster_path:image_url+movie.poster_path
                    };
                });
            }
        }
    });

    // Initialize the Bloodhound suggestion engine
    movies.initialize();
    // Instantiate the Typeahead UI
    $('.typeahead').typeahead(null, {
        displayKey: 'value',
        source: movies.ttAdapter(),
        templates: {
            suggestion: Handlebars.compile("<p style='padding:6px'><img width=50 src='{{poster_path}}'> <b>{{value}}</b> - Release date {{release_date}} </p>"),
            footer: Handlebars.compile("<b>Searched for '{{query}}'</b>")
        }
    });


    var anime = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('anime_english_title'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
            url: 'meep.php?query=%QUERY'
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
            // source: anime.ttAdapter(),
            hint: false,
            minLength: 3
        },
        confirmKeys: [13, 44, 188],
        maxTags: 5,
        freeInput: false,
        delimiter: '|'
    });
});

 // Anime Search



