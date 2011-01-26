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
    this.siteTitle = document.title;

    $.ajaxSetup({
        timeout: 60000
    });

    this.entryTitleToSidebarFromURL = function(box, url) {
        var theThis = this;
        $.getJSON(url, function(json) {
            var s = new StringBuffer();
            $.each(json, function() {
                s.append('<li><a href="#!').append(this['url']).append('" title="').
                    append(this['title']).append('" class="withBorder">').
                    append(this['omitted_title']).
                    append('</a></li>\n');
            });
            box.append(s.toString());
        });
    };

/*    this.bindOnClickEventToLinkUsingBox = function(box, page, scroll) {
        var theThis = this;
        $.each(box.find('a[href^="#!"]'), function() {
            var url = $(this).attr('href');
            url = theThis.convertJsonURLFromPath(url.split('#!', 2)[1]);
            // console.log(url);
            $(this).click(function() {
                theThis.entriesToContentFromURL(url, page, scroll);
            });
        });
    };*/

    this.beforeActionToLoadContent = function(scroll) {
        if (scroll !== "no") {
            // $(document).scrollTop(this.contentBox.prev().offset().top);
            // $(document).scrollTop($('#menubar').offset().top);
            $('html, body').animate({scrollTop: $('#menubar').offset().top},
                                    {easing: 'easeInOutCirc',
                                     duration: 500});
        }
        this.contentBox.hide();
        this.contentBox.empty();
        this.loadingImage.show();
    };

    this.errorActionToLoadContent = function(xhr, status) {
        alert('ajax error!');
    };

    this.completeActionToLoadContent = function(scroll) {
        this.loadingImage.hide();
        this.beautyOfCodeActionToLoadContent(scroll);
    };

    this.beautyOfCodeActionToLoadContent = function(scroll) {
        if (scroll !== "no") {
            $.beautyOfCode.beautifyAll();
        } else {
            $.beautyOfCode.init('clipboard.swf');
        }
    };

    this.articleContent = function(box, jsonLength, json) {
        var s = new StringBuffer();
        s.append('<article class="entry">').
            append('<header class="entryHeader"><h3 class="green">').
            append(json['title']).append('</h3></header>').
            append('<time pubdate="').append(json['attr_created']).append('" class="pubdate">').
            append(json['display_created']).append('</time>').
            append(json['body']).
            append('<nav class="entryFooter"></nav>');

        if (json['tags'].length > 0) {
            s.append('<nav class="entryTags"><ul>');
            $.each(json['tags'], function() {
                s.append('<li><a href="#!').append(this['url']).append('">').
                    append(this['name']).append('</a></li>');
            });
            s.append('</ul></nav>');
        }
        s.append('</article>');
        box.append(innerShiv(s.toString()));

        if (jsonLength > 1) {
            var url = json['url'];
            var json_url = json['json_url'];
            var title = json['title'];
            box.find('h3:last').wrapInner('<a></a>').children().attr({
                href: '#!' + url,
                title: title
            }).append('<span class="white permalink">link</span>');
        }
        if (json['rel_entries'].length > 0) {
            var tmp = box.find('nav.entryFooter:last').append('<ul></ul>').children('ul');
            $.each(json['rel_entries'], function() {
                var s = new StringBuffer();
                s.append('<li>').
                    append('<a href="#!').append(this['url']).append('">').
                    append(this['title']).append('</a>').
                    append('</li>');
                tmp.append(innerShiv(s.toString()));
            });
        }
        // box.find('article:last').show('drop');
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
                // box.empty();
                $.each(json['entries'], function() {
                    theThis.articleContent(box, jsonLength, this);
                });
                box.show('drop');
                theThis.randomRotateImage(box);
                theThis.applyLazyload(box);

                if (typeof json['paginator'] !== 'undefined') {
                    box.find('h3 a').addClass('plain blue');
                    box.find('.permalink').addClass('bgBlue');

                    var paginator = json['paginator'];
                    if (String(paginator['has_other_pages']) == 'true') {
                        var s = new StringBuffer('<nav id="moreEntries"><ul>');
                        if (String(paginator['has_previous']) == 'true') {
                            s.append('<li><a href="#!/blog/recents/').
                                append(paginator['previous_page_number']).append('/">&lt;').append('</a></li>');
                        }
                        if (String(paginator['has_next']) == 'true') {
                            s.append('<li><a href="#!/blog/recents/').
                                append(paginator['next_page_number']).append('/">&gt; つぎの5けん……').append('</a></li>');
                        }
                        box.append(innerShiv(s.append('</ul></nav>').toString()));
                    }
                    // theThis.moreEntriesLink(page);
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

    this.moreEntriesLink = function(page) {
        if (!page) {
            page = 1;
        }
        var tmpPage = page+1;
        var box = this.contentBox;
        var theThis = this;
        var s = new StringBuffer();
        s.append('<div id="moreEntries">').
            append('<a href="#!/blog/recents/').append(tmpPage).append('/">つぎの5けん……</a>').
            append('</div>');
        box.append(s.toString());
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
                // box.empty();
                var s = new StringBuffer('<nav class="archives">');
                var currentYear = '';
                $.each(json, function() {
                    if (currentYear === '') {
                        s.append('<div class="year">').append(this['year']).append(' - ').
                            append('<ul>');
                        currentYear = this['year'];
                    } else if (currentYear !== this['year']) {
                        s.append('</ul></div>\n').append('<div class="year">').
                            append(this['year']).append(' - <ul>');
                        currentYear = this['year'];
                    }
                    s.append('<li><a href="#!').append(this['url']).append('">').
                        append(this['month']).append('</a></li>');
                });
                s.append('</ul></nav>');
                box.append(innerShiv(s.toString()));
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
                var previousArchive = json['previous_archive'][0];
                var nextArchive = json['next_archive'][0];
                // box.empty();
                box.append(innerShiv(new StringBuffer('<header id="entriesHeader" class="orange">“').
                                     append(currents).append('”な記事').
                                     append('</header>').toString()));
                var nav = new StringBuffer('<nav class="entriesNav"><ul>');
                if (nextArchive) {
                    nav.append('<li><a href="#!').append(nextArchive['url']).
                        // append(nextArchive['year']).append('/').append(nextArchive['month']).
                        append('" class="withBorder">').append('&lt;').append('</a></li>');
                }
                nav.append('<li>').append(currents).append('</li>');
                if (previousArchive) {
                    nav.append('<li><a href="#!').append(previousArchive['url']).
                        append('" class="withBorder">').append('&gt;').append('</a></li>');
                }
                nav.append('</ul></nav>');
                nav = nav.toString();
                box.append(innerShiv(nav));
                $.each(json['entries'], function() {
                    theThis.articleContent(box, jsonLength, this);
                });

                if (typeof json['paginator'] !== 'undefined') {
                    var paginator = json['paginator'];
                    if (String(paginator['has_other_pages']) == 'true') {
                        var s = new StringBuffer('<nav id="moreEntries"><ul>');
                        if (String(paginator['has_previous']) == 'true') {
                            s.append('<li><a href="#!').append(currentArchive['url']).
                                append(paginator['previous_page_number']).append('/">&lt;').append('</a></li>');
                        }
                        if (String(paginator['has_next']) == 'true') {
                            s.append('<li><a href="#!').append(currentArchive['url']).
                                append(paginator['next_page_number']).append('/">&gt; つぎの10けん……').append('</a></li>');
                        }
                        box.append(innerShiv(s.append('</ul></nav>').toString()));
                    }
                }
                box.append(innerShiv(nav));
                box.show('drop');
                theThis.randomRotateImage(box);
                theThis.applyLazyload(box);


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
                // var titles = json['titles'];
                var paginator = json['paginator'];
                var tag = json['tag'][0];
                box.empty();
                box.append(innerShiv(new StringBuffer('<header id="entriesHeader" class="orange">“').
                                     append(tag['name']).append('”な記事').
                                     append('</header>').toString()));
                var nav = new StringBuffer('<nav class="entriesNav"><ul>');
                if (String(paginator['has_previous']) == 'true') {
                    nav.append('<li><a href="#!').append(tag['url']).
                        append(paginator['previous_page_number']).append('/').append('" class="withBorder">').
                        append('&lt;').append('</a></li>');
                }
                nav.append('<li class="pagePerPages">').append(paginator['num_page']).append(' / ').
                    append(paginator['num_pages']).append('</li>');
                if (String(paginator['has_next']) == 'true') {
                    nav.append('<li><a href="#!').append(tag['url']).
                        append(paginator['next_page_number']).append('/').append('" class="withBorder">').
                        append('&gt;').append('</a></li>');
                }
                nav.append('</ul></nav>');
                nav = nav.toString();
                box.append(innerShiv(nav));
                // var s = new StringBuffer('<nav class="tagTitles"><ul>');
                // $.each(titles, function() {
                //     s.append('<li>').append(this['title']).append('</li>');
                // });
                // s.append('</ul></nav>');
                // box.append(innerShiv(s.toString()));
                $.each(entries, function() {
                    theThis.articleContent(box, jsonLength, this);
                });
                box.append(innerShiv(nav));
                box.show('drop');
                theThis.randomRotateImage(box);
                theThis.applyLazyload(box);

                box.find('h3 a').addClass('plain green');
                box.find('.permalink').addClass('bgGreen');

                document.title = new StringBuffer(theThis.siteTitle).
                    append('・').append(tag['name']).toString();
            },
            url: url
        });

    };

    this.applyLazyload = function(box) {
        if (!this.isMobile) {
            $.each(box.find('img'), function() {
                $(this).lazyload({
                    placeholder : "/site_media/js/2.0/lazyload/grey.gif",
                    effect : "fadeIn",
                    threshold : 200
                });
            });
        }
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
};

$(function() {
    var loader = new ReiAreLoader();
    loader.entryTitleToSidebarFromURL($('#recentEntries'), '/blog/api/recents/title.json');

    var url  = location.href;
    var path = url.split('#!', 2)[1];
    if ((path) && (path.match(/^\/blog\/.+/))) {
        if (path.indexOf('/recents/') > -1) {
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
        loader.entriesToContentFromURL('/blog/api/recents/1/entry.json', 1, 'no');
    }

    $(window).hashchange(function() {
        var path = '/blog/';
        if (location.hash) {
            path = location.hash.split('#!', 2)[1];
        }
        if (path.match(/^\/blog\/$/)) {
            loader.entriesToContentFromURL('/blog/api/recents/1/entry.json', 1);
        } else if (path.indexOf('/recents/') > -1) {
            var page = path.split('/').reverse()[1];
            loader.entriesToContentFromURL(loader.convertJsonURLFromPath(path), parseInt(page, 10));
        } else if (path.indexOf('/archives/') > -1) {
            loader.archiveTitlesToContent();
        } else if (path.indexOf('/tag/') > -1) {
            loader.tagEntriesToContent(loader.convertJsonURLFromPath(path));
        } else if(path.match(/^\/blog\/\d{4}\/\d{2}\/(\d\/)?$/)) {
            loader.archiveEntriesToContent(loader.convertJsonURLFromPath(path));
        } else {
            loader.entriesToContentFromURL(loader.convertJsonURLFromPath(path));
        }
    });
});
