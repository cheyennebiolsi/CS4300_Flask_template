$(document).ready(function() {
   setAnimeExplanation(); 
   setWordExplanation();
    // Stop Format on 
//    $("#submit").click(function() {
//        $('#myform').submit();
//    });

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
    $('.animeinput .tt-input').focusin(function() {
//        console.log('called');
        console.log($(this).position());
 //       console.log($('#wordinput').offset());
    });
});

function setAnimeExplanation() {
    var text = "Enter anime into the search bar to receive suggestions based on<br>shows that you are famililar with.<br><br>" + 
               "<b>Note:</b> clicking on tags changes their functionality<br>" +
               "A <span class='tag label label-primary'>green</span> background returns results that are similar to that anime<br>" +
               "A <span class='tag label label-danger'>red</span> background returns results that are dissimilar to that anime<br>"
    $(document.querySelector(".animeinput i")).attr("data-original-title", text);
    $(document.querySelector(".animeinput .tt-hint")).attr("data-original-title", "Search limited to 3 anime");
}

function setWordExplanation() {
    var text = "Enter keywords into the search bar to receive suggestions based on how closely<br>related the themes of the anime are to the keyword.<br><br>" + 
               "<b>Note:</b> clicking on tags changes their functionality<br>" +
               "A <span class='tag label label-primary'>GREEN</span> background returns results whose themes are closely related to the keyword<br>" +
               "A <span class='tag label label-danger'>RED</span> background returns results whose themes are unrelated to the keyword<br>"
    $(document.querySelector(".wordinput i")).attr("data-original-title", text);
    $(document.querySelector(".wordinput .tt-hint")).attr("data-original-title", "Search limited to 5 keywords");
}

function createLegend() { 
    document.getElementById('chart-legends').innerHTML = anime_scores.generateLegend();
};

function toggleClass(selector, tag) {
    if (tag.sign == "positive") {
        selector.classList.remove("label-primary")
        selector.classList.add("label-danger");
        tag.sign = "negative";
    } else {
        selector.classList.remove("label-danger")
        selector.classList.add("label-primary");
        tag.sign = "positive";
    };
}

function resizeAnimeSearchBar() {
        tags = $('.animeinput .tag');
        if (tags.length == 0) {return};
        var firstPosition = $(tags.get(0)).position().top;
        var lastPosition = $(tags.get(-1)).position().top;
        console.log("Last position " + lastPosition);
        console.log("First position " + firstPosition);
        var mod = Math.floor((lastPosition - firstPosition)/28);
        $('.animeinput .bootstrap-tagsinput').css("height", 36 + 28*mod + "px");
        var input = document.querySelector(".animeinput .bootstrap-tagsinput").getBoundingClientRect();
        var lastTag = tags.get(-1).getBoundingClientRect();
        console.log(input);
        console.log(lastTag);
        if (input.right - lastTag.right < 150) {
            $('.animeinput .bootstrap-tagsinput').css("height", 36 + 28*(mod+1) + "px");
        };
        var searchBar = document.querySelector(".animeinput .bootstrap-tagsinput").getBoundingClientRect();
        $('.animeinput .input-group-prepend span').css("line-height", searchBar.height -2 + "px");
}

function resizeWordSearchBar() {
        tags = $('.wordinput .tag');
        if (tags.length == 0) {return};
        var firstPosition = $(tags.get(0)).position().top;
        var lastPosition = $(tags.get(-1)).position().top;
        console.log("Last position " + lastPosition);
        console.log("First position " + firstPosition);
        var mod = Math.floor((lastPosition - firstPosition)/28);
        $('.wordinput .bootstrap-tagsinput').css("height", 36 + 30*mod + "px");
        var input = document.querySelector(".wordinput .bootstrap-tagsinput").getBoundingClientRect();
        var lastTag = tags.get(-1).getBoundingClientRect();
        console.log(input);
        console.log(lastTag);
        if (input.right - lastTag.right < 100) {
            $('.wordinput .bootstrap-tagsinput').css("height", 36 + 30*(mod+1) + "px");
        };
        var searchBar = document.querySelector(".wordinput .bootstrap-tagsinput").getBoundingClientRect();
        $('.wordinput .input-group-prepend span').css("line-height", searchBar.height -2 + "px");
}
function initializeSearchBars() {
    var animeTags = [];
    var wordTags = [];

    $(document).on("click", ".wordinput .tag", function() {
        var selector = $(this).get(0);
        var tagTitle = $(this).text();
        wordTags.forEach(function(tag) {
            if (tag.word == tagTitle) {
                toggleClass(selector, tag);
            }
        });
    });

    $(document).on("click", ".animeinput .tag", function() {
        var selector = $(this).get(0);
        var tagTitle = $(this).text();
        animeTags.forEach(function(tag) {
            if (tag.anime_english_title == tagTitle) {
                toggleClass(selector, tag);
//                tag.sign = (tag.sign == "positive") ? "negative" : "positive";
                
            }
        });
        console.log(animeTags);
//        $('#animeinput').tagsinput('remove', {anime_english_title: $(this).text()});
    });

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
        tagClass: function(item) {
            switch (item.sign) {
                case 'positive' : return 'label label-primary';
                case 'negative' : return 'label label-danger';
                default: return 'label label-info';
            }
        },
        itemValue: 'word',
        typeaheadjs: {
            displayKey: 'word',
            source: word.ttAdapter(),
            hint: true,
            minLength: 3
        },
        confirmKeys: [13, 44, 188],
        maxTags: 7,
        freeInput: false,
        delimiter: '|'
    });
    $('body').tooltip({selector: '[rel=tooltip]'});
    $('.wordinput .tt-hint').attr('data-toggle', 'tooltip');
    $('.wordinput .tt-hint').attr('data-placement', 'right');
    $('#wordinput').on('itemAdded', function(event) {
        resizeWordSearchBar();
        wordTags.push(event.item);
    });
    $('.wordinput').on('beforeItemAdd', function(event) {
        if (wordTags.length >= 5) {
            event.cancel = true;
            $('.wordinput .tt-hint').tooltip({trigger: "manual", placement: "right"});
            $('.wordinput .tt-hint').tooltip('show');
            setTimeout(function() {
                $('.wordinput .tt-hint').tooltip('hide');
            }, 3000);
        };
    });
    $('#wordinput').on('itemRemoved', function(event) {
        resizeWordSearchBar();
        wordTags = $.grep(wordTags, function(query) { return query.word !== event.item.word; });
    });

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
        tagClass: function(item) {
            switch (item.sign) {
                case 'positive' : return 'label label-primary';
                case 'negative' : return 'label label-danger';
                default: return 'label label-info';
            }
        },
        delimiter: '|',
        itemValue: 'anime_english_title',
        typeaheadjs: {
            displayKey: 'anime_english_title',
            templates: {
                suggestion: function (data) {
                    return '<div class="d-flex">' +
                               '<img class="align-self-center mr-3" src="' + data.anime_image_url + '">' +
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
        maxTags: 7,
        freeInput: false,
    });
    $('.animeinput .tt-hint').attr('data-toggle', 'tooltip');
    $('.animeinput .tt-hint').attr('data-placement', 'right');
//    $('.animeinput .tt-input').attr('data-delay', 5000);
//    $('.animeinput .tt_input').attr('data-original-title', 'meow');
    $('.animeinput').on('itemAdded', function(event) {
        resizeAnimeSearchBar();
        animeTags.push(event.item);
    });
    $('.animeinput').on('beforeItemAdd', function(event) {
        console.log("here " + animeTags.length)
        if (animeTags.length >= 3) {
            event.cancel = true;
            $('.animeinput .tt-hint').tooltip({trigger: "manual", placement: "right"});
            $('.animeinput .tt-hint').tooltip('show');
            setTimeout(function() {
                $('.animeinput .tt-hint').tooltip('hide');
            }, 3000);
//            $('.animeinput .tt-input').tooltip('dispose');
          //  $(document.querySelector('input#animeinput')).attr('placeholder', '');
          //  console.log($(document.querySelector('input#animeinput')));
          //  $('#animeinput').tagsinput('refresh');
          //    $('input#animeinput').blur(function(){jQuery(this).attr('placeholder', '')});
        };
    });
    $('#animeinput').on('itemRemoved', function(event) {
        resizeAnimeSearchBar();
        animeTags = $.grep(animeTags, function(query) { return query.anime_english_title !== event.item.anime_english_title; });
    });

    $('#myform').submit(function() {
        let animeInput = [];
        animeTags.forEach(function(query) {
            animeInput.push(((query.sign == "positive") ? "" : "!") + query.anime_english_title)
        });
        $('#animeinput').val(animeInput.join("|"));

        let wordInput = [];
        wordTags.forEach(function(query) {
            wordInput.push(((query.sign == "positive") ? "" : "!") + query.word);
        });
        $('#wordinput').val(wordInput.join("|"));
        console.log($(this));
        $(this).children('#animeinput').remove();
        processFilters();
        return true;
    });
//    $('[data-toggle="tooltip"]').tooltip().tooltip('hide');
};

function processFilters() {
    var filterVals = []
    $('input[type="checkbox"]').each(function(index) {
        let name = $(this).attr('name');
        let checked = $(this).is(":checked");
        if (name !== undefined) {
            if (checked) {filterVals.push(name)};
            $(this).removeAttr('name');
        };
    });
    var encodedFilter = window.btoa(filterVals.join("&"));
    $('<input/>').attr('type', 'hidden')
                 .attr('name', 'filters')
                 .attr('value', encodedFilter)
                 .appendTo('#myform');
    return
};

function initializeWordSearch(wordList) {
    for (var word in wordList) {
        let tag = wordList[word];
        let sign = "positive"
        if (tag.slice(0, 1) == "!") {
            tag = tag.slice(1,);
            sign = "negative";
        };
        $('#wordinput').tagsinput('add', {word: tag, sign: sign});
    ;}
};

function initializeAnimeSearch(animeList) {
    for (var anime in animeList) {
        let tag = $("<div/>").html(animeList[anime]).text();
        let sign = "positive"
        if (tag.slice(0, 1) == "!") {
            tag = tag.slice(1,);
            sign = "negative";
        };
        console.log("Initializing anime search with " + tag);
        $('#animeinput').tagsinput('add', {anime_english_title: tag, sign: sign});
    ;}
};
