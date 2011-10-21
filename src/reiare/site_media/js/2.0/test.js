module('StringBuffer', {
    setup: function() {
        this.empty = new StringBuffer();
        this.aString = new StringBuffer('a');
        this.manyStrings = new StringBuffer('a').append('b').append('c');
    }
});
test('StringBuffer', function() {
    same('', this.empty.toString());
    same(this.aString.buffer[0], 'a');
    same(this.manyStrings.toString(), 'abc');
});

module('ReiAreLoader', {
    setup: function() {
        this.loader = new ReiAreLoader();
        this.loader.randomRotateImage($('#imgBox'));
        this.contentBox = $('#content');
        this.jsons = {"entries": [{"body": "<p>test body.</p>",
                                   "display_created": "2011/8/25 (\u6728) a.m.12:06",
                                   "rel_entries": [],
                                   "url": "/blog/2011/08/25/reikai-11-9-announce/",
                                   "title": "test title.",
                                   "attr_created": "2011-08-25T00:06:55+0900",
                                   "tags": [{"url": "/blog/tag/tag1/", "id": 16, "name": "tag1"},
                                            {"url": "/blog/tag/tag2/", "id": 40, "name": "tag2"},
                                            {"url": "/blog/tag/tag3/", "id": 17, "name": "tag3"}],
                                   "id": 3595},
                                  {"body": "<p>test body2.</p>",
                                   "display_created": "2011/8/25 (\u6728) a.m.12:06",
                                   "rel_entries": [],
                                   "url": "/blog/2011/08/25/reikai-11-9-announce/",
                                   "title": "test title2.",
                                   "attr_created": "2011-08-25T00:06:55+0900",
                                   "tags": [{"url": "/blog/tag/tag1/", "id": 16, "name": "tag1"},
                                            {"url": "/blog/tag/tag2/", "id": 40, "name": "tag2"},
                                            {"url": "/blog/tag/tag3/", "id": 17, "name": "tag3"}],
                                   "id": 3596}]};
    }
});
test('isMobile', function() {
    ok(!(this.loader.isMobile));
});
test('isIE', function() {
    ok(!(this.loader.isIE));
});
test('siteTitle', function() {
    deepEqual(this.loader.siteTitle, '例のあれ（仮題）');
});
test('randomRotateImage', function() {
    ok($('#rotateImage').css('-webkit-transform'));
});
test('convertJsonURLFromPath', function() {
    deepEqual(this.loader.convertJsonURLFromPath('/blog/'), '/blog/api/entry.json');
    deepEqual(this.loader.convertJsonURLFromPath('/blog/recents/'), '/blog/api/recents/entry.json');
    deepEqual(this.loader.convertJsonURLFromPath('/blog/recents/2/'), '/blog/api/recents/2/entry.json');
    deepEqual(this.loader.convertJsonURLFromPath('/blog/archives/'), '/blog/api/archives/title.json');
    deepEqual(this.loader.convertJsonURLFromPath('/blog/tag/'), '/blog/api/tag/entry.json');
    deepEqual(this.loader.convertJsonURLFromPath('/blog/tag/django/'), '/blog/api/tag/django/entry.json');
});
test('beforeActionToLoadContent', function() {
    this.loader.beforeActionToLoadContent('no');
    deepEqual(this.contentBox.css('display'), 'none');
    deepEqual(this.contentBox.html(), '');
    deepEqual($('#loadingImageBox').css('display'), 'block');
/*    console.log($('#menubar').offset());
    console.log($('#dummy').scrollTop());*/
});
test('completeActionToLoadContent', function() {
    this.loader.completeActionToLoadContent('no');
    deepEqual($('#loadingImageBox').css('display'), 'none');
});
test('showIncludeEntries', function() {
    this.loader.showIncludeEntries($('#content'));
    deepEqual(this.contentBox.css('display'), 'block');
});
asyncTest('entryTitleToSidebarFromURL', function() {
    var theThis = this;
    theThis.loader.entryTitleToSidebarFromURL(this.contentBox, '/blog/api/recents/title.json');
    setTimeout(function() {
        ok(((theThis.contentBox.html()).indexOf('<li><a href="#!/blog/') > -1));
        start();
    }, 500);
});
test('articleContent', function() {
    this.contentBox.empty();
    this.loader.articleContent(this.contentBox, 1, this.jsons['entries'][0]);
    deepEqual(this.contentBox.html(), '<article class="entry">     <header class="entryHeader"><h3 class="green">test title.<span class="white permalink bgGreen"><a href="/blog/2011/08/25/reikai-11-9-announce/" data-ajax="false" class="plain green">link</a></span></h3></header>     <time pubdate="2011-08-25T00:06:55+0900" class="pubdate">2011/8/25 (木) a.m.12:06</time>     <p>test body.</p>                 <nav class="entryTags">         <ul>                    <li><a href="#!/blog/tag/tag1/">tag1</a></li>                    <li><a href="#!/blog/tag/tag2/">tag2</a></li>                    <li><a href="#!/blog/tag/tag3/">tag3</a></li>                  </ul>       </nav>        </article>');
/*    ok(((this.contentBox.html()).indexOf('<article class="entry">') > -1));
    ok(((this.contentBox.html()).indexOf('<nav class="entryTags">') > -1));*/
    this.contentBox.empty();
    this.loader.articleContent(this.contentBox, 2, this.jsons['entries'][1]);
    deepEqual(this.contentBox.html(), '<article class="entry">     <header class="entryHeader"><h3 class="green"><a href="#!/blog/2011/08/25/reikai-11-9-announce/" title="test title2.">test title2.</a><span class="white permalink"><a href="/blog/2011/08/25/reikai-11-9-announce/" data-ajax="false">link</a></span></h3></header>     <time pubdate="2011-08-25T00:06:55+0900" class="pubdate">2011/8/25 (木) a.m.12:06</time>     <p>test body2.</p>                 <nav class="entryTags">         <ul>                    <li><a href="#!/blog/tag/tag1/">tag1</a></li>                    <li><a href="#!/blog/tag/tag2/">tag2</a></li>                    <li><a href="#!/blog/tag/tag3/">tag3</a></li>                  </ul>       </nav>        </article>');
});
asyncTest('entriesToContentFromURL', function() {
    var theThis = this;
    theThis.loader.entriesToContentFromURL(theThis.loader.convertJsonURLFromPath('/blog/2011/08/24/django-offline-docs/'));
    setTimeout(function() {
        deepEqual(theThis.contentBox.html(), '<article class="entry">     <header class="entryHeader"><h3 class="green">Django Offline Docs（非公式）。<span class="white permalink bgGreen"><a href="/blog/2011/08/24/django-offline-docs/" data-ajax="false" class="plain green">link</a></span></h3></header>     <time pubdate="2011-08-24T23:26:24+0900" class="pubdate">2011/8/24 (水) p.m.11:26</time>     <p>　<a href="http://sramana.in/dod/">Django Offline Docs</a></p>\n\n<p>　DjangoさんのDocumentはPython製のFrameworkらしくエゲツナイ程の充実度を放っておりますが、「オンライン版だけでオフライン版がないよ、ないんだよ」って事で作ってみてくれたみたいです。</p>\n\n<p>　最近の事情を鑑みますとオフラインである事はあまりないと思いますけども、PDF版などは違う使い方もできますし、ローカルに持っておいてサクサク参照するのもいいかもしれないですね。</p>                 <nav class="entryTags">         <ul>                    <li><a href="#!/blog/tag/django/">django</a></li>                    <li><a href="#!/blog/tag/document/">document</a></li>                    <li><a href="#!/blog/tag/python/">python</a></li>                  </ul>       </nav>        </article>');
        start();
    }, 500);
});
asyncTest('entriesToContentFromURL recents', function() {
    var theThis = this;
    theThis.loader.entriesToContentFromURL(theThis.loader.convertJsonURLFromPath('/blog/recents/1/'));
    setTimeout(function() {
        var contentValue = theThis.contentBox.html();
        var result = contentValue.match(/<article class="entry">*/g);
        equal(result.length, 5);
        start();
    }, 500);
});
asyncTest('archiveTitlesToContent', function() {
    var theThis = this;
    theThis.loader.archiveTitlesToContent();
    setTimeout(function() {
        ok(theThis.contentBox.html().match(/^<nav class="archives">.|\n*<\/nav>$/));
        start();
    }, 500);
});
asyncTest('tagEntriesToContent', function() {
    var theThis = this;
    theThis.loader.tagEntriesToContent(theThis.loader.convertJsonURLFromPath('/blog/tag/apple/'));
    setTimeout(function() {
        var contentValue = theThis.contentBox.html();
        ok(contentValue.match(/^<header id="entriesHeader" class="orange">“apple”な記事<\/header><nav class="entriesNav">.*/));
        var result = contentValue.match(/<article class="entry">*/g);
        equal(result.length, 10);
        start();
    }, 500);
});
asyncTest('pjax', function () {
    $('#pjaxLink').click();
    setTimeout(function () {
        var contentValue = $('#content').html();
        deepEqual(contentValue, '\n<article class=\"entry\">\n<header class=\"entryHeader\">\n  \n  \n    <h3 class=\"green\" data-title=\"WebObjectsにGWTを統合するwogwt。\">WebObjectsにGWTを統合するwogwt<span style=\"letter-spacing:-0.25em\">。</span></h3>\n  \n  \n</header>\n<time pubdate=\"2011-10-14T17:40:52+0900\" class=\"pubdate\">2011/10/14 (金) p.m.05:40</time>\n<p>　<a href=\"http://code.google.com/p/wogwt/\">wogwt - WebObjects and GWT integration - Google Project Hosting</a></p>\n\n<p>　メモをひっくり返していたら目についた。例によって試してもいない。それだけ……。</p>\n\n\n<nav class=\"entryTags\"><ul>\n\n  <li><a href=\"/blog/tag/java/\">java</a></li>\n\n  <li><a href=\"/blog/tag/software/\">software</a></li>\n\n  <li><a href=\"/blog/tag/webobjects/\">webobjects</a></li>\n\n</ul></nav>\n\n</article>\n');
        start();
    }, 1000);
});
