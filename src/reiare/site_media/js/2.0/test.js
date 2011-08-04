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
        this.loader.convertShebang();
        this.loader.randomRotateImage($('#imgBox'));
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
test('convertShebang', function() {
    deepEqual($('#shebangLink').attr('href'), '#!/blog/spam/');
    deepEqual($('#staticLink').attr('href'), '/blog/ham/');
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
asyncTest('entryTitleToSidebarFromURL', function() {
    var theThis = this;
    theThis.loader.entryTitleToSidebarFromURL($('#content'), '/blog/api/recents/title.json');
   setTimeout(function() {
       console.log($('#content').html());
       ok((($('#content').html()).indexOf('<li><a href="#!/blog/') > -1));
       start();
   }, 100);
});

// test("a basic test example", function() {
//          ok( true, "this test is fine" );
//          var value = "hello";
//          equals( "hello", value, "We expect value to be hello" );
//      });

// module("Module A");

// test("first test within module", function() {
//          ok( true, "all pass" );
//      });

// test("second test within module", function() {
//          ok( true, "all pass" );
//      });

// module("Module B");

// test("some other test", function() {
//          expect(2);
//          equals( true, false, "failing test" );
//          equals( true, true, "passing test" );
//          //});

//      });
