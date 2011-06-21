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
