var StringBuffer = function(string) {
    this.buffer = [];

    this.append = function(string) {
        this.buffer.push(string);
        return this;
    };

    this.toString = function() {
        return this.buffer.join('');
    };

    if (string) {
        this.append(string);
    }
};

var ReiAreLoader = function() {
    this.isMobile = (navigator.userAgent.indexOf('Mobile') != -1);
    this.isIE = /*@cc_on!@*/!1;
    this.contentBox = $('#content');
    this.loadingImage = $('#loadingImageBox');
    this.siteTitle = '例のあれ（仮題）';

    $.ajaxSetup({
        timeout: 60000
    });

    this.entryTitleToSidebarFromURL = function(box, url) {
        var theThis = this;
        $.getJSON(url, function(json) {
            $('#entryTitleToSidebarTemplate').tmpl(json).appendTo(box);
        });
    };

    this.beforeActionToLoadContent = function(scroll) {
        if (scroll !== "no") {
            $('html, body').animate({scrollTop: $('#menubar').offset().top},
                                    {easing: 'easeInOutCirc',
                                     duration: 500});
        }
        this.contentBox.hide();
        this.contentBox.empty();
        this.loadingImage.show();
    };

    this.errorActionToLoadContent = function(xhr, status) {
        alert('読み込みに失敗しました。\nリロードしてみてくださいませ。');
    };

    this.completeActionToLoadContent = function(scroll) {
        this.loadingImage.hide();
        this.beautyOfCodeActionToLoadContent(scroll);
        this.flAutoKerning();
    };

    this.beautyOfCodeActionToLoadContent = function(scroll) {
        if (scroll !== "no") {
            $.beautyOfCode.beautifyAll();
        } else {
            $.beautyOfCode.init('clipboard.swf');
        }
    };

    this.flAutoKerning = function() {
        if ($('.entryHeader h3 a').length > 0) {
            $('.entryHeader h3 a').flAutoKerning();
        } else {
            $('.entryHeader h3').flAutoKerning();
        }
    };

    this.articleContent = function(box, jsonLength, json) {
        var tmp = $('<div></div>');
        $('#entryArticleTemplate').tmpl(json).appendTo(tmp);
        box.append(innerShiv(tmp.html(), false));

        if (jsonLength > 1) {
            var url = json['url'];
            var json_url = json['json_url'];
            var title = json['title'];
            box.find('h3:last').wrapInner('<a></a>').children().attr({
                href: '#!' + url,
                title: title
            }).parent().append(
                new StringBuffer('<span class="white permalink"><a href="').
                    append(url).append('" data-ajax="false">link</a></span>').toString());
        } else if (jsonLength == 1) {
            var url = json['url'];
            var json_url = json['json_url'];
            var title = json['title'];
            box.find('h3').append(new StringBuffer('<span class="white permalink bgGreen"><a href="').
                                  append(url).append('" data-ajax="false" class="plain green">link</a></span>').toString());
        }
    };

    this.entriesToContentFromURL = function(url, page, scroll) {
        var box = this.contentBox;
        var loading = this.loadingImage;
        var theThis = this;
        $.ajax({
            beforeSend: function() {
                theThis.beforeActionToLoadContent(scroll);
            },
            complete: function() {
                theThis.completeActionToLoadContent(scroll);
            },
            dataType: 'json',
            error: function (xhr, status) {
                theThis.errorActionToLoadContent(xhr, status);
            },
            success: function(json) {
                var jsonLength = json['entries'].length;
                $.each(json['entries'], function() {
                    theThis.articleContent(box, jsonLength, this);
                });
                box.show('drop');
                theThis.randomRotateImage(box);

                if (typeof json['paginator'] !== 'undefined') {
                    box.find('h3 a').addClass('plain blue');
                    box.find('.permalink').addClass('bgBlue');

                    var paginator = json['paginator'];
                    if (String(paginator['has_other_pages']) == 'true') {
                        var tmp = $('<div></div>');
                        $('#moreEntriesTemplate').tmpl(paginator, {
                            'previousUrl': function() {
                                return new StringBuffer('#!/blog/recents/').
                                    append(this.data.previous_page_number).append('/').toString();
                            },
                            'nextUrl': function() {
                                return new StringBuffer('#!/blog/recents/').
                                    append(this.data.next_page_number).append('/').toString();
                            }
                        }).appendTo(tmp);
                        box.append(innerShiv(tmp.html(), false));
                    }
                } else if (jsonLength > 1) {
                    box.find('h3 a').addClass('plain green');
                    box.find('.permalink').addClass('bgGreen');
                }

                if (jsonLength == 1) {
                    document.title = new StringBuffer(theThis.siteTitle).
                        append('・').append(json['entries'][0]['title']).toString();
                } else {
                    document.title = theThis.siteTitle;
                }
            },
            url: url
        });
    };

    this.archiveTitlesToContent = function(scroll) {
        var box = this.contentBox;
        var loading = this.loadingImage;
        var theThis = this;
        $.ajax({
            beforeSend: function() {
                theThis.beforeActionToLoadContent(scroll);
            },
            complete: function() {
                theThis.completeActionToLoadContent(scroll);
            },
            dataType: 'json',
            error: function (xhr, status) {
                theThis.errorActionToLoadContent(xhr, status);
            },
            success: function(json) {
                var tmp = $('<div></div>');
                $('#archivesTemplate').tmpl({month: json}, {
                    currentYear: '',
                    yearString: function(month) {
                        if (this.currentYear === '') {
                            this.currentYear = month['year'];
                            return true;
                        }
                        return false;
                    },
                    updateYearString: function(month) {
                        if (this.currentYear !== month['year']) {
                            this.currentYear = month['year'];
                            return true;
                        }
                        return false;
                    }
                }).appendTo(tmp);
                box.append(innerShiv(tmp.html(), false));
                box.show('drop');

                document.title = new StringBuffer(theThis.siteTitle).
                    append('・').append('あーかいぶ').toString();
            },
            url: '/blog/api/archives/title.json'
        });
    };

    this.archiveEntriesToContent = function(url, scroll) {
        var box = this.contentBox;
        var loading = this.loadingImage;
        var theThis = this;
        $.ajax({
            beforeSend: function() {
                theThis.beforeActionToLoadContent(scroll);
            },
            complete: function() {
                theThis.completeActionToLoadContent(scroll);
            },
            dataType: 'json',
            error: function (xhr, status) {
                theThis.errorActionToLoadContent(xhr, status);
            },
            success: function(json) {
                var jsonLength = json['entries'].length;
                var currentArchive = json['current_archive'][0];
                var currents = new StringBuffer(currentArchive['year']).append('/').
                    append(currentArchive['month']).toString();
                $('#entriesHeaderTemplate').tmpl({'currents': currents}).appendTo(box);
                var tmp = $('<div></div>');
                $('#entriesNavTemplate').tmpl({'currents': currents,
                                               'previousArchive': json['previous_archive'][0],
                                               'nextArchive': json['next_archive'][0]}).appendTo(tmp);
                var nav = tmp.html();
                box.append(innerShiv(nav, false));
                $.each(json['entries'], function() {
                    theThis.articleContent(box, jsonLength, this);
                });

                if (typeof json['paginator'] !== 'undefined') {
                    var paginator = json['paginator'];
                    if (String(paginator['has_other_pages']) == 'true') {
                        tmp = $('<div></div>');
                        $('#moreEntriesTemplate').tmpl(paginator, {
                            'previousUrl': function() {
                                return new StringBuffer('#!').
                                    append(currentArchive['url']).
                                    append(this.data.previous_page_number).append('/').toString();
                            },
                            'nextUrl': function() {
                                return new StringBuffer('#!').
                                    append(currentArchive['url']).
                                    append(this.data.next_page_number).append('/').toString();
                            }
                        }).appendTo(tmp);
                        box.append(innerShiv(tmp.html(), false));
                    }
                }
                box.append(innerShiv(nav, false));
                box.show('drop');
                theThis.randomRotateImage(box);

                box.find('h3 a').addClass('plain green');
                box.find('.permalink').addClass('bgGreen');

                document.title = new StringBuffer(theThis.siteTitle).
                    append('・').append(currents).toString();
            },
            url: url
        });
    };

    this.tagEntriesToContent = function(url, scroll) {
        var box = this.contentBox;
        var loading = this.loadingImage;
        var theThis = this;
        $.ajax({
            beforeSend: function() {
                theThis.beforeActionToLoadContent(scroll);
            },
            complete: function() {
                theThis.completeActionToLoadContent(scroll);
            },
            dataType: 'json',
            error: function (xhr, status) {
                theThis.errorActionToLoadContent(xhr, status);
            },
            success: function(json) {
                var entries = json['entries'];
                var jsonLength = entries.length;
                var paginator = json['paginator'];
                var tag = json['tag'][0];

                $('#entriesHeaderTemplate').tmpl({'currents': tag['name']}).appendTo(box);
                var tmp = $('<div></div>');
                $('#entriesNavForTagsTemplate').tmpl(paginator, {
                    'tagUrl': tag['url']}).appendTo(tmp);
                var nav = tmp.html();
                box.append(innerShiv(nav, false));
                $.each(entries, function() {
                    theThis.articleContent(box, jsonLength, this);
                });
                box.append(innerShiv(nav, false));
                box.show('drop');
                theThis.randomRotateImage(box);

                box.find('h3 a').addClass('plain green');
                box.find('.permalink').addClass('bgGreen');

                document.title = new StringBuffer(theThis.siteTitle).
                    append('・').append(tag['name']).toString();
            },
            url: url
        });

    };

    this.convertJsonURLFromPath = function(path) {
        var baseUrl = new StringBuffer(path.replace(/^\/blog\//, '/blog/api/'));
        if (path.indexOf('/recents/') > -1) {
            return baseUrl.append('entry.json').toString();
        } else if (path.indexOf('/archives/') > -1) {
            return baseUrl.append('title.json').toString();
        } else if (path.indexOf('/tag/') > -1) {
            return baseUrl.append('entry.json').toString();
        } else {
            return baseUrl.append('entry.json').toString();
        }
    };

    this.randomRotateImage = function(box) {
        if (!this.isIE) {
            $.each(box.find('img'), function() {
                var deg = Math.random() * 3 - 1.5;
                var s = new StringBuffer('rotate(').append(deg).append('deg)').toString();
                $(this).css("transform", s).
                    css("-webkit-transform", s).css("-moz-transform", s);
            });
        }
    };

    this.showIncludeEntries = function(box) {
        this.loadingImage.show();
        this.randomRotateImage(box);
        this.completeActionToLoadContent('no');
        box.show('drop');
    };
};

$(function() {
    var loader = new ReiAreLoader();

    var url  = location.href;
    var path = url.split('#!', 2)[1];

    if ((path) && (path.match(/^\/blog\/+/))) {
        if (path.match(/^\/blog\/$/)) {
            loader.entriesToContentFromURL('/blog/api/recents/1/entry.json', 1, 'no');
        } else if (path.indexOf('/recents/') > -1) {
            var page = path.split('/').reverse()[1];
            loader.entriesToContentFromURL(loader.convertJsonURLFromPath(path), parseInt(page, 10), 'no');
        } else if (path.indexOf('/archives/') > -1) {
            loader.archiveTitlesToContent('no');
        } else if (path.indexOf('/tag/') > -1) {
            loader.tagEntriesToContent(loader.convertJsonURLFromPath(path), 'no');
        } else if(path.match(/^\/blog\/\d{4}\/\d{2}\/(\d\/)?$/)) {
            loader.archiveEntriesToContent(loader.convertJsonURLFromPath(path), 'no');
        } else {
            loader.entriesToContentFromURL(loader.convertJsonURLFromPath(path), null, 'no');
        }
    } else {
       loader.showIncludeEntries($('#content'));
    }

    $('a[data-pjax]').pjax();
    $('#content p > a[href^="/blog/"]').pjax('#content');
    $('#content').bind('pjax:start', function () {
        $(this).hide();
        $('#loadingImageBox').show();
        $('html, body').animate({scrollTop: $('#menubar').offset().top},
                                {easing: 'easeInOutCirc'});
    }).bind('pjax:end', function () {
        if ($(this).find('h3').length === 1) {
            document.title = new StringBuffer(loader.siteTitle).
                    append('- ').append(($(this).find('h3')).data('title')).toString();
        } else if ($(this).find('#entriesHeader').length > 0) {
            document.title = new StringBuffer(loader.siteTitle).
                    append('- ').append($(this).find('#entriesHeader').data('title')).toString();
        } else {
            document.title = loader.siteTitle;
        }
        loader.beautyOfCodeActionToLoadContent();
        loader.flAutoKerning();
        loader.randomRotateImage($(this));
        loader.loadingImage.hide();
        $(this).show('drop');
    });
});
