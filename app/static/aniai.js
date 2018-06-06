$(document).ready(function() {
   setAnimeExplanation(); 
   setWordExplanation();   
   $('[data-toggle="collapse"]').click(function(e) {
            if($($(this).data('target')).hasClass('collapsing'))
            return false;
   });
});

function redirectHomepage() {
    window.location.href="/";
};

function toggle(source) {
    var checkboxes = document.querySelectorAll('#sfwgenre');
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i] != source) {
            checkboxes[i].checked = source.checked;
        };
    };
    if ((document.querySelector('#sfw-button').checked)) {
        var checkboxes = document.querySelectorAll('#nsfwgenre');
        for (var i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = source.checked;
        }
    };
};

function clearnsfw(source) {
    if (source.checked) {
    var genres = document.querySelectorAll('#nsfwgenre');
    for (var i = 0; i < genres.length; i++) {
        genres[i].checked = true;
    };
    var ratings = document.querySelectorAll('#nsfwrating');
    for (var i = 0; i < ratings.length; i++) {
        ratings[i].checked = true;
        };
    };
};

function getNext(index) {
    var nextDisplay = $($('.owl-item').not('.cloned')[index]).find('.view')[0];
    console.log(nextDisplay);
    changeRecommendedDisplay(nextDisplay);
}

function changeRecommendedDisplay(source) {
                    $('#recommended-display').css('opacity', 0);
                    setTimeout(function() {
                            $('#recommended-display').css('opacity', 1);
        	            var active = (document.querySelectorAll('.well.suggestion.active'));
                            active.forEach(function(well) {
                            well.classList.remove('active');
                        });
                    var children = $('.owl-item').find('.well.suggestion');
                    var anime_index = $(source).attr('data-index');
                    children.each(function(index) {
                        console.log($(this).data('index'));
                        console.log(anime_index);
                        if ($(this).data('index') == anime_index) {
                            this.classList.add('active');
                        };
                    }).bind(anime_index);
                    var anime_image_url = $(source).data("image");
                    var title = $(source).data("title");
                    var type = $(source).data("type");
                    var synopsis = $(source).data("synopsis");
                    var tags = $(source).data("tags");
                    var words = $(source).data("words");
                    var episode_count = $(source).data("episodes");
                    var duration = $(source).data("duration");
                    var rating = $(source).data("rating");
                    var overall = $(source).data("overallreview");  
                    var story = $(source).data("storyreview");  
                    var enjoyment = $(source).data("enjoyment");  
                    var character = $(source).data("character");  
                    var sound = $(source).data("sound");  
                    var animation = $(source).data("animation");
                    var similarity = $(source).data("similarity");
                    var reviewernumber = $(source).data("reviewernumber");
                    var raternumber = $(source).data("raternumber");
                    var ratingvalue = $(source).data("ratingvalue");
                    var thelabels = $(source).data("labels");
                    var thevalues = $(source).data("values");
                    var posiitive_words = $(source).data("positive_words");
                    var original_value = $(source).data("original_value");
                    $('#media-image').attr('src', anime_image_url);
                    $('#media-title span').text(title);
                    document.getElementById('plus-icon').innerHTML = "<i onclick='addAnime(" + '"' + title + '"' + ")' class='fa fa-plus'></i>";
                    $('#media-type span').text(type);
                    $('#media-rating span').text(rating);
                    $('#media-count span').text(episode_count);
                    $('#media-duration span').text(duration);
                    $('#media-synopsis span').text(synopsis);
                    $('#episode-count span').text(episode_count);
                    $('#similarity-score span').text(similarity);
                    $('#reviewer-number span').text("Number of Reviewers: " + reviewernumber);
                    $('#rater-number span').text("Number of Raters: " + raternumber);
                    $('#rating-value span').text("Rating: " + ratingvalue);
                    var tags = tags.split("|");
                    var str = "";
                    for (var tag in tags) {
                        str += '<span class="genre">' + tags[tag] + "</span>";
                    };
                    var words = words.split("|");
                    var wordStr = "";
                    for (var word in words) {
                        wordStr += '<span class="tag label label-info" onclick="addWord(source)">' + words[word] + "</span>";
                    };
                    $('#anime-tags').replaceWith(
                        '<div class="align-self-start unselectable" id="anime-tags">' + wordStr + '</div>'
                        );
                    $('#media-genres').replaceWith(
                        '<div class="media-genres unselectable" id="media-genres">' + str + '</div>'
                        );
                    var anime_video_url = $(source).data("video");
                    if (anime_video_url.includes('crunchyroll')) {
                        $('#video-link').attr("href", anime_video_url);
                        $('#video-link').attr("hidden", false);
                        $('#crunchyroll-provider-image').attr("hidden", false);
                        $('#crunchyroll-provider').attr("hidden", false);
                        $('#hulu-provider').attr("hidden", true);
                        $('#yahoo-provider').attr("hidden", true);
                    } else if (anime_video_url.includes('yahoo')) {
                        $('#video-link').attr("href", anime_video_url);
                        $('#video-link').attr("hidden", false);
                        $('#yahoo-provider').attr("hidden", false);
                        $('#hulu-provider').attr("hidden", true);
                        $('#crunchyroll-provider-image').attr("hidden", true);
                        $('#crunchyroll-provider').attr("hidden", true);
                    } else if (anime_video_url.includes('hulu')) {
                        $('#hulu-provider').attr("hidden", false);
                        $('#yahoo-provider').attr("hidden", true);
                        $('#video-link').attr("href", anime_video_url);
                        $('#video-link').attr("hidden", false);
                        $('#crunchyroll-provider-image').attr("hidden", true);
                        $('#crunchyroll-provider').attr("hidden", true);
                    } else {
                        $('#video-link').attr("href", anime_video_url);
                        $('#video-link').attr("hidden", true);
                        $('#crunchyroll-provider-image').attr("hidden", true);
                        $('#crunchyroll-provider').attr("hidden", true);
                        $('#hulu-provider').attr("hidden", true);
                        $('#yahoo-provider').attr("hidden", true);
                    };
                    var suggestionIndex = $(source).data('suggestionindex');
                    var numSuggestions = $(source).data('num');
                    document.getElementById('nextSuggested').setAttribute("onClick", "getNext(" + (suggestionIndex + 1) % numSuggestions + ")");
                    document.getElementById('prevSuggested').setAttribute("onClick", "getNext(" + (suggestionIndex - 1) % numSuggestions + ")");
                    anime_scores.destroy(); //delete charts
                    var thelabels2 = thelabels.split("|");
                    anime_scores = createChart("vis", "anime_scores", title, thelabels2, original_value, thevalues);
                    createLegend('chart-legends', anime_scores);
                    }.bind(source), 750);
                };

$(document).on("click", ".collapse.show .show-info .fa", function() {
   $(this).tooltip({trigger: "manual", placement: "top"});
   $(this).tooltip('show');
   setTimeout(function() {
       $(this).tooltip('hide');
   }.bind(this), 8000);
});

function setAnimeExplanation() {
    var text = "Enter anime into the search bar to receive suggestions based on<br>shows that you are famililar with.<br><br>" + 
               "<b>Note:</b> clicking on tags changes their functionality<br>" +
               "A <span class='tag label label-primary'>green</span> background returns results that are similar to that anime<br>" +
               "A <span class='tag label label-danger'>red</span> background returns results that are dissimilar to that anime<br>"
    $(document.querySelector(".animeinput .input-group-prepend i")).attr("data-original-title", text);
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

function createLegend(chart_legends_id, chartName) { 
    document.getElementById(chart_legends_id).innerHTML = chartName.generateLegend();
    
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
        animeTags.push(event.item);
    });
    $('.animeinput').on('beforeItemAdd', function(event) {
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

function addAnime(title) {
   console.log(title);
   $('#animeinput').tagsinput('add', {anime_english_title: title, sign: "positive"});
}

function addWord(tag) {
    $('#wordinput').tagsinput('add', {word: $(tag).text(), sign: "positive"});
};

function initializeAnimeSearch(animeList) {
    for (var anime in animeList) {
        let tag = $("<div/>").html(animeList[anime]).text();
        let sign = "positive"
        if (tag.slice(0, 1) == "!") {
            tag = tag.slice(1,);
            sign = "negative";
        };
        $('#animeinput').tagsinput('add', {anime_english_title: tag, sign: sign});
    ;}
};

function createChart(chartId, chartName, title, thelabels2, original_value, thevalues) {
    Chart.defaults.global.defaultFontColor = "white";
    var data_chart = {
    labels: thelabels2,
                    datasets: [
                        {
                            label: "Query",
                            fill: true,
                            backgroundColor: "rgba(152,251,152,0.2)",
                            borderColor: "rgba(152,251,152,1)",
                            pointBorderColor: "#fff",
                            pointBackgroundColor: "rgba(152,251,152,0.2)",
                            pointBorderColor: "#fff",
                            data: original_value
                        },
                        {
                            label: title,
                            fill: true,
                            backgroundColor: "rgba(219,112,147,0.2)",
                            borderColor: "rgba(219,112,147,1)",
                            pointBorderColor: "#fff",
                            pointBackgroundColor: "rgba(219,112,147,1)",
                            pointBorderColor: "#fff",
                            data: thevalues
                        }
                    ]
                    };
			    return new Chart(document.getElementById(chartId), {
				type: 'radar',
				data: data_chart,
				draggable: true,
				options: { 
                                            legendCallback: function(chart) {
                                                var queryLabel = chart.data.datasets[0].label;
                                                var queryColor = chart.data.datasets[0].backgroundColor;
                                                var queryBorder = chart.data.datasets[0].borderColor;
                                                var suggestionLabel = chart.data.datasets[1].label;
                                                var suggestionColor = chart.data.datasets[1].backgroundColor;
                                                var suggestionBorder = chart.data.datasets[1].borderColor;
                                                var text = 
                                                '<label class="fancy-checkbox">' +
                                                     '<input type="checkbox" onclick="toggleLegendQuery(this, ' + chartName + ')" checked/>' +
                                                     '<div class="legend-tag checked" id="query-unchecked">' + 
                                                     '<div class="legend-button" style="background-color:' + queryColor + '; border-color: ' + queryBorder + '">' + 
                                                     '</div>' + queryLabel + '</div>' + 
                                                     '<div class="legend-tag unchecked" id="query-checked">' + 
                                                     '<div class="legend-button" style="background-color:' + queryColor + '; border-color: ' + queryBorder + '">' +
                                                     '</div>' + queryLabel + '</div></label>' + 
                                                '<label class="fancy-checkbox">' +
                                                     '<input type="checkbox" onclick="toggleLegendSuggestion(this, ' + chartName + ')" checked/>' +
                                                     '<div class="legend-tag checked" id="suggestion-checked">' + 
                                                     '<div class="legend-button" style="background-color:' + suggestionColor + '; border-color: ' + suggestionBorder + '">' +
                                                     '</div>' + suggestionLabel + '</div>' + 
                                                     '<div class="legend-tag unchecked" id="suggestion-unchecked">' +
                                                     '<div class="legend-button" style="background-color:' + suggestionColor + '; border-color: ' + suggestionBorder + '">' + 
                                                     '</div>' + suggestionLabel + '</div></label>';
                                                return text;
                                            },
                                            hover: {
                                                onHover: function(e) {
                                                    var activePoints = this.getElementAtEvent(e);
                                                    if (activePoints[0] !== undefined) {
                                                        e.target.style.cursor = "pointer";
                                                    } else {
                                                       e.target.style.cursor = "default";
                                                    }
                                                }
                                            },
                            title: {
                                display: true,
                                text: 'Most Similar Words to Query',
                                fontColor: "#FFFFFF",
                                fontSize: 14
                            },
                            legend: {
                                display: false,
                                position: 'bottom',
                                boxWidth: 20,
                                labels: {
                                    fontColor: '#FFFFFF'
                                },
                            },
                            scale: {
                                ticks: {
                                    maxTicksLimit: 5,
                                    backdropColor: 'black',
                                    max: Math.floor(Math.min(10*(Math.max.apply(Math, original_value.concat(thevalues)) + 0.1), 10))/10,
                                    min: 0, 
                                    fontSize: 6,
                                    color: '#FFFFFF'
                                },
                                gridLines: {
                                    color: "#FFFFFF"
                                }
                            },
                                            tooltips: {
                                                footerFontStyle: 'normal',
                                                callbacks: {
                                                    footer: function(tooltipItem, data) {
                                                        var label = data.labels[tooltipItem[0].index];
                                                        return ['Click to add "' + label + '" to search bar'];
                                                    },
                                                    label: function(tooltipItem, data) {
                                                    var datasetLabel = '';
                                                    var label = data.datasets[tooltipItem.datasetIndex].label;
                                                    return data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index] + " " + label;
                                                    }
                                                },
                                                enabled: true,
                                                mode: 'index'
                                            },
                            responsive: true,
                            maintainAspectRatio: false,
                        }
                    });
};
