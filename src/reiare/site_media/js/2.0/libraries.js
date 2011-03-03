/* jquery.beautyOfCode-min.js  */
jQuery.beautyOfCode={settings:{autoLoad:true,baseUrl:'/site_media/js/2.0/beautyofcode/syntaxhighlighter_2.1.364/',scripts:'scripts/',styles:'styles/',theme:'Default',brushes:['Xml','Python','JScript','Plain'],config:{},defaults:{},ready:function(){jQuery.beautyOfCode.beautifyAll();}},init:function(settings){settings=jQuery.extend({},jQuery.beautyOfCode.settings,settings);if(!settings.config.clipboardSwf)
settings.config.clipboardSwf=settings.baseUrl+settings.scripts+'clipboard.swf';jQuery(document).ready(function(){if(!settings.autoLoad){settings.ready();}
else{jQuery.beautyOfCode.utils.loadCss(settings.baseUrl+settings.styles+'shCore.css');jQuery.beautyOfCode.utils.loadCss(settings.baseUrl+settings.styles+'shTheme'+settings.theme+'.css','shTheme');var scripts=new Array();scripts.push(settings.baseUrl+settings.scripts+'shCore.js');jQuery.each(settings.brushes,function(i,item){scripts.push(settings.baseUrl+settings.scripts+'shBrush'+item+".js");});jQuery.beautyOfCode.utils.loadAllScripts(scripts,function(){if(settings&&settings.config)
jQuery.extend(SyntaxHighlighter.config,settings.config);if(settings&&settings.defaults)
jQuery.extend(SyntaxHighlighter.defaults,settings.defaults);settings.ready();});}});},beautifyAll:function(){jQuery("pre.code:has(code[class]),code.code").beautifyCode();},utils:{loadScript:function(url,complete){jQuery.ajax({url:url,complete:function(){complete();},type:'GET',dataType:'script',cache:true});},loadAllScripts:function(urls,complete){if(!urls||urls.length==0)
{complete();return;}
var first=urls[0];jQuery.beautyOfCode.utils.loadScript(first,function(){jQuery.beautyOfCode.utils.loadAllScripts(urls.slice(1,urls.length),complete);});},loadCss:function(url,id){var headNode=jQuery("head")[0];if(url&&headNode)
{var styleNode=document.createElement('link');styleNode.setAttribute('rel','stylesheet');styleNode.setAttribute('href',url);if(id)styleNode.id=id;headNode.appendChild(styleNode);}},addCss:function(css,id){var headNode=jQuery("head")[0];if(css&&headNode)
{var styleNode=document.createElement('style');styleNode.setAttribute('type','text/css');if(id)styleNode.id=id;if(styleNode.styleSheet){styleNode.styleSheet.cssText=css;}
else{jQuery(styleNode).text(css);}
headNode.appendChild(styleNode);}},addCssForBrush:function(brush,highlighter){if(brush.isCssInitialized)
return;jQuery.beautyOfCode.utils.addCss(highlighter.Style);brush.isCssInitialized=true;},parseParams:function(params){var trimmed=jQuery.map(params,jQuery.trim);var paramObject={};var getOptionValue=function(name,list){var regex=new RegExp('^'+name+'\\[([^\\]]+)\\]$','gi');var matches=null;for(var i=0;i<list.length;i++)
if((matches=regex.exec(list[i]))!=null)
return matches[1];return null;}
var handleValue=function(flag){var flagValue=getOptionValue('boc-'+flag,trimmed);if(flagValue)paramObject[flag]=flagValue;};handleValue('class-name');handleValue('first-line');handleValue('tab-size');var highlight=getOptionValue('boc-highlight',trimmed);if(highlight)paramObject['highlight']=jQuery.map(highlight.split(','),jQuery.trim);var handleFlag=function(flag){if(jQuery.inArray('boc-'+flag,trimmed)!=-1)
paramObject[flag]=true;else if(jQuery.inArray('boc-no-'+flag,trimmed)!=-1)
paramObject[flag]=false;};handleFlag('smart-tabs');handleFlag('ruler');handleFlag('gutter');handleFlag('toolbar');handleFlag('collapse');handleFlag('auto-links');handleFlag('light');handleFlag('wrap-lines');handleFlag('html-script');return paramObject;}}};jQuery.fn.beautifyCode=function(brush,params){var saveBrush=brush;var saveParams=params;this.each(function(i,item){var $item=jQuery(item);var $code=$item.is('code')?$item:$item.children("code");var code=$code[0];var classItems=code.className.replace(/.+?(brush:|language-)/,'$1').replace('language-','').split(" ");var brush=saveBrush?saveBrush:classItems[0];var elementParams=jQuery.beautyOfCode.utils.parseParams(classItems);var params=jQuery.extend({},SyntaxHighlighter.defaults,saveParams,elementParams);if(params['html-script']=='true')
{highlighter=new SyntaxHighlighter.HtmlScript(brush);}
else
{var brush=SyntaxHighlighter.utils.findBrush(brush);if(brush)
highlighter=new brush();else
return;}
jQuery.beautyOfCode.utils.addCssForBrush(brush,highlighter);if($item.is("pre")&&($code=$item.children("code")))
$item.text($code.text());highlighter.highlight($item.html(),params);highlighter.source=item;$item.replaceWith(highlighter.div);});};

/* jquery.lazyload.min.js */
(function($){$.fn.lazyload=function(options){var settings={threshold:0,failurelimit:0,event:"scroll",effect:"show",container:window};if(options){$.extend(settings,options);}
var elements=this;if("scroll"==settings.event){$(settings.container).bind("scroll",function(event){var counter=0;elements.each(function(){if($.abovethetop(this,settings)||$.leftofbegin(this,settings)){}else if(!$.belowthefold(this,settings)&&!$.rightoffold(this,settings)){$(this).trigger("appear");}else{if(counter++>settings.failurelimit){return false;}}});var temp=$.grep(elements,function(element){return!element.loaded;});elements=$(temp);});}
this.each(function(){var self=this;if(undefined==$(self).attr("original")){$(self).attr("original",$(self).attr("src"));}
if("scroll"!=settings.event||undefined==$(self).attr("src")||settings.placeholder==$(self).attr("src")||($.abovethetop(self,settings)||$.leftofbegin(self,settings)||$.belowthefold(self,settings)||$.rightoffold(self,settings))){if(settings.placeholder){$(self).attr("src",settings.placeholder);}else{$(self).removeAttr("src");}
self.loaded=false;}else{self.loaded=true;}
$(self).one("appear",function(){if(!this.loaded){$("<img />").bind("load",function(){$(self).hide().attr("src",$(self).attr("original"))
[settings.effect](settings.effectspeed);self.loaded=true;}).attr("src",$(self).attr("original"));};});if("scroll"!=settings.event){$(self).bind(settings.event,function(event){if(!self.loaded){$(self).trigger("appear");}});}});$(settings.container).trigger(settings.event);return this;};$.belowthefold=function(element,settings){if(settings.container===undefined||settings.container===window){var fold=$(window).height()+$(window).scrollTop();}else{var fold=$(settings.container).offset().top+$(settings.container).height();}
return fold<=$(element).offset().top-settings.threshold;};$.rightoffold=function(element,settings){if(settings.container===undefined||settings.container===window){var fold=$(window).width()+$(window).scrollLeft();}else{var fold=$(settings.container).offset().left+$(settings.container).width();}
return fold<=$(element).offset().left-settings.threshold;};$.abovethetop=function(element,settings){if(settings.container===undefined||settings.container===window){var fold=$(window).scrollTop();}else{var fold=$(settings.container).offset().top;}
return fold>=$(element).offset().top+settings.threshold+$(element).height();};$.leftofbegin=function(element,settings){if(settings.container===undefined||settings.container===window){var fold=$(window).scrollLeft();}else{var fold=$(settings.container).offset().left;}
return fold>=$(element).offset().left+settings.threshold+$(element).width();};$.extend($.expr[':'],{"below-the-fold":"$.belowthefold(a, {threshold : 0, container: window})","above-the-fold":"!$.belowthefold(a, {threshold : 0, container: window})","right-of-fold":"$.rightoffold(a, {threshold : 0, container: window})","left-of-fold":"!$.rightoffold(a, {threshold : 0, container: window})"});})(jQuery);

/*
 * jQuery hashchange event - v1.3 - 7/21/2010
 * http://benalman.com/projects/jquery-hashchange-plugin/
 *
 * Copyright (c) 2010 "Cowboy" Ben Alman
 * Dual licensed under the MIT and GPL licenses.
 * http://benalman.com/about/license/
 */
(function($,e,b){var c="hashchange",h=document,f,g=$.event.special,i=h.documentMode,d="on"+c in e&&(i===b||i>7);function a(j){j=j||location.href;return"#"+j.replace(/^[^#]*#?(.*)$/,"$1")}$.fn[c]=function(j){return j?this.bind(c,j):this.trigger(c)};$.fn[c].delay=50;g[c]=$.extend(g[c],{setup:function(){if(d){return false}$(f.start)},teardown:function(){if(d){return false}$(f.stop)}});f=(function(){var j={},p,m=a(),k=function(q){return q},l=k,o=k;j.start=function(){p||n()};j.stop=function(){p&&clearTimeout(p);p=b};function n(){var r=a(),q=o(m);if(r!==m){l(m=r,q);$(e).trigger(c)}else{if(q!==m){location.href=location.href.replace(/#.*/,"")+q}}p=setTimeout(n,$.fn[c].delay)}$.browser.msie&&!d&&(function(){var q,r;j.start=function(){if(!q){r=$.fn[c].src;r=r&&r+a();q=$('<iframe tabindex="-1" title="empty"/>').hide().one("load",function(){r||l(a());n()}).attr("src",r||"javascript:0").insertAfter("body")[0].contentWindow;h.onpropertychange=function(){try{if(event.propertyName==="title"){q.document.title=h.title}}catch(s){}}}};j.stop=k;o=function(){return a(q.location.href)};l=function(v,s){var u=q.document,t=$.fn[c].domain;if(v!==s){u.title=h.title;u.open();t&&u.write('<script>document.domain="'+t+'"<¥/script>');u.close();q.location.hash=v}}})();return j})()})(jQuery,this);

// http://jdbartlett.github.com/innershiv | WTFPL License
window.innerShiv=(function(){var d,r;return function(h,u){if(!d){d=document.createElement('div');r=document.createDocumentFragment();/*@cc_on d.style.display = 'none'@*/}var e=d.cloneNode(true);/*@cc_on document.body.appendChild(e);@*/e.innerHTML=h.replace(/^¥s¥s*/, '').replace(/¥s¥s*$/, '');/*@cc_on document.body.removeChild(e);@*/if(u===false)return e.childNodes;var f=r.cloneNode(true),i=e.childNodes.length;while(i--)f.appendChild(e.firstChild);return f}}());

/*
 * jQuery Easing v1.3 - http://gsgd.co.uk/sandbox/jquery/easing/
 *
 * Uses the built in easing capabilities added In jQuery 1.1
 * to offer multiple easing options
 *
 * TERMS OF USE - jQuery Easing
 *
 * Open source under the BSD License.
 *
 * Copyright ﾂｩ 2008 George McGinley Smith
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *
 * Redistributions of source code must retain the above copyright notice, this list of
 * conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice, this list
 * of conditions and the following disclaimer in the documentation and/or other materials
 * provided with the distribution.
 *
 * Neither the name of the author nor the names of contributors may be used to endorse
 * or promote products derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 *  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 *  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
 *  GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 *  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGE.
 *
*/

// t: current time, b: begInnIng value, c: change In value, d: duration
jQuery.easing.jswing=jQuery.easing.swing;jQuery.extend(jQuery.easing,{def:"easeOutQuad",swing:function(e,f,a,h,g){return jQuery.easing[jQuery.easing.def](e,f,a,h,g)},easeInQuad:function(e,f,a,h,g){return h*(f/=g)*f+a},easeOutQuad:function(e,f,a,h,g){return -h*(f/=g)*(f-2)+a},easeInOutQuad:function(e,f,a,h,g){if((f/=g/2)<1){return h/2*f*f+a}return -h/2*((--f)*(f-2)-1)+a},easeInCubic:function(e,f,a,h,g){return h*(f/=g)*f*f+a},easeOutCubic:function(e,f,a,h,g){return h*((f=f/g-1)*f*f+1)+a},easeInOutCubic:function(e,f,a,h,g){if((f/=g/2)<1){return h/2*f*f*f+a}return h/2*((f-=2)*f*f+2)+a},easeInQuart:function(e,f,a,h,g){return h*(f/=g)*f*f*f+a},easeOutQuart:function(e,f,a,h,g){return -h*((f=f/g-1)*f*f*f-1)+a},easeInOutQuart:function(e,f,a,h,g){if((f/=g/2)<1){return h/2*f*f*f*f+a}return -h/2*((f-=2)*f*f*f-2)+a},easeInQuint:function(e,f,a,h,g){return h*(f/=g)*f*f*f*f+a},easeOutQuint:function(e,f,a,h,g){return h*((f=f/g-1)*f*f*f*f+1)+a},easeInOutQuint:function(e,f,a,h,g){if((f/=g/2)<1){return h/2*f*f*f*f*f+a}return h/2*((f-=2)*f*f*f*f+2)+a},easeInSine:function(e,f,a,h,g){return -h*Math.cos(f/g*(Math.PI/2))+h+a},easeOutSine:function(e,f,a,h,g){return h*Math.sin(f/g*(Math.PI/2))+a},easeInOutSine:function(e,f,a,h,g){return -h/2*(Math.cos(Math.PI*f/g)-1)+a},easeInExpo:function(e,f,a,h,g){return(f==0)?a:h*Math.pow(2,10*(f/g-1))+a},easeOutExpo:function(e,f,a,h,g){return(f==g)?a+h:h*(-Math.pow(2,-10*f/g)+1)+a},easeInOutExpo:function(e,f,a,h,g){if(f==0){return a}if(f==g){return a+h}if((f/=g/2)<1){return h/2*Math.pow(2,10*(f-1))+a}return h/2*(-Math.pow(2,-10*--f)+2)+a},easeInCirc:function(e,f,a,h,g){return -h*(Math.sqrt(1-(f/=g)*f)-1)+a},easeOutCirc:function(e,f,a,h,g){return h*Math.sqrt(1-(f=f/g-1)*f)+a},easeInOutCirc:function(e,f,a,h,g){if((f/=g/2)<1){return -h/2*(Math.sqrt(1-f*f)-1)+a}return h/2*(Math.sqrt(1-(f-=2)*f)+1)+a},easeInElastic:function(f,h,e,l,k){var i=1.70158;var j=0;var g=l;if(h==0){return e}if((h/=k)==1){return e+l}if(!j){j=k*0.3}if(g<Math.abs(l)){g=l;var i=j/4}else{var i=j/(2*Math.PI)*Math.asin(l/g)}return -(g*Math.pow(2,10*(h-=1))*Math.sin((h*k-i)*(2*Math.PI)/j))+e},easeOutElastic:function(f,h,e,l,k){var i=1.70158;var j=0;var g=l;if(h==0){return e}if((h/=k)==1){return e+l}if(!j){j=k*0.3}if(g<Math.abs(l)){g=l;var i=j/4}else{var i=j/(2*Math.PI)*Math.asin(l/g)}return g*Math.pow(2,-10*h)*Math.sin((h*k-i)*(2*Math.PI)/j)+l+e},easeInOutElastic:function(f,h,e,l,k){var i=1.70158;var j=0;var g=l;if(h==0){return e}if((h/=k/2)==2){return e+l}if(!j){j=k*(0.3*1.5)}if(g<Math.abs(l)){g=l;var i=j/4}else{var i=j/(2*Math.PI)*Math.asin(l/g)}if(h<1){return -0.5*(g*Math.pow(2,10*(h-=1))*Math.sin((h*k-i)*(2*Math.PI)/j))+e}return g*Math.pow(2,-10*(h-=1))*Math.sin((h*k-i)*(2*Math.PI)/j)*0.5+l+e},easeInBack:function(e,f,a,i,h,g){if(g==undefined){g=1.70158}return i*(f/=h)*f*((g+1)*f-g)+a},easeOutBack:function(e,f,a,i,h,g){if(g==undefined){g=1.70158}return i*((f=f/h-1)*f*((g+1)*f+g)+1)+a},easeInOutBack:function(e,f,a,i,h,g){if(g==undefined){g=1.70158}if((f/=h/2)<1){return i/2*(f*f*(((g*=(1.525))+1)*f-g))+a}return i/2*((f-=2)*f*(((g*=(1.525))+1)*f+g)+2)+a},easeInBounce:function(e,f,a,h,g){return h-jQuery.easing.easeOutBounce(e,g-f,0,h,g)+a},easeOutBounce:function(e,f,a,h,g){if((f/=g)<(1/2.75)){return h*(7.5625*f*f)+a}else{if(f<(2/2.75)){return h*(7.5625*(f-=(1.5/2.75))*f+0.75)+a}else{if(f<(2.5/2.75)){return h*(7.5625*(f-=(2.25/2.75))*f+0.9375)+a}else{return h*(7.5625*(f-=(2.625/2.75))*f+0.984375)+a}}}},easeInOutBounce:function(e,f,a,h,g){if(f<g/2){return jQuery.easing.easeInBounce(e,f*2,0,h,g)*0.5+a}return jQuery.easing.easeOutBounce(e,f*2-g,0,h,g)*0.5+h*0.5+a}});

/*
 *
 * TERMS OF USE - EASING EQUATIONS
 *
 * Open source under the BSD License.
 *
 * Copyright ﾂｩ 2001 Robert Penner
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *
 * Redistributions of source code must retain the above copyright notice, this list of
 * conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice, this list
 * of conditions and the following disclaimer in the documentation and/or other materials
 * provided with the distribution.
 *
 * Neither the name of the author nor the names of contributors may be used to endorse
 * or promote products derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 *  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 *  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
 *  GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 *  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 */

/*
 * @class FLAutoKerning
 * @version 0.0.3 (2011/02/28)
 *
 * テキストに文字詰めを適用するUtilityクラス。
 * インスタンス化せずに、スタティック関数として使用する。
 *
 * @author Takayuki Fukatsu, artandmobile.com, fladdict.net
 * @requires jQuery
 */
(function(b){var c={};c["*う"]=-0.03;c["う*"]=-0.02;c["*く"]=-0.075;c["く*"]=-0.075;c["*し"]=-0.075;c["し*"]=-0.075;c["*ぁ"]=-0.05;c["ぁ*"]=-0.075;c["*ぃ"]=-0.05;c["ぃ*"]=-0.075;c["*ぅ"]=-0.05;c["ぅ*"]=-0.075;c["*ぇ"]=-0.05;c["ぇ*"]=-0.075;c["*ぉ"]=-0.05;c["ぉ*"]=-0.075;c["*っ"]=-0.075;c["っ*"]=-0.075;c["*ゃ"]=-0.05;c["ゃ*"]=-0.075;c["*ゅ"]=-0.05;c["ゅ*"]=-0.075;c["*ょ"]=-0.075;c["ょ*"]=-0.075;c["*ト"]=-0.075;c["ト*"]=-0.075;c["*ド"]=-0.075;c["ド*"]=-0.075;c["*リ"]=-0.075;c["リ*"]=-0.075;c["*ッ"]=-0.05;c["ッ*"]=-0.075;c["ャ*"]=-0.05;c["*ャ"]=-0.05;c["ュ*"]=-0.05;c["*ュ"]=-0.05;c["ョ*"]=-0.08;c["*ョ"]=-0.08;c["*「"]=-0.25;c["」*"]=-0.25;c["*（"]=-0.25;c["）*"]=-0.25;c["、*"]=-0.25;c["。*"]=-0.25;c["・*"]=-0.25;c["*・"]=-0.25;c["*："]=-0.25;c["：*"]=-0.25;c["して"]=-0.12;c["す。"]=-0.15;c["タク"]=-0.12;c["タグ"]=-0.12;c["ット"]=-0.2;c["ラム"]=-0.1;c["プル"]=-0.1;c["ンプ"]=-0.15;c["ング"]=-0.05;c["ード"]=-0.15;c["」「"]=-0.75;c["」。"]=-0.25;c["」、"]=-0.25;c["、「"]=-0.75;c["。「"]=-0.75;c["、『"]=-0.75;c["。『"]=-0.75;c["、（"]=-0.75;c["。（"]=-0.75;c["「"]=-0.5;c["『"]=-0.5;c["（"]=-0.5;c["【"]=-0.5;c["“"]=-0.5;var a={};a.DEFAULT_KERNING_INFO=c;a.process=function(d,e){if(e==undefined){e=a.DEFAULT_KERNING_INFO}d.each(function(q,k){var m=b(k).html();var g="";var j=m.length;for(var l=0;l<j;l++){var p=m.substr(l,1);var o=p;var h=m.substr(l+1,1);var f=0;if(e[p+h]){f=e[p+h]}else{if(e[p+"*"]){f+=e[p+"*"]}if(e["*"+h]){f+=e["*"+h]}}if(f!==0){o="<span style='letter-spacing:"+f+"em'>"+p+"</span>"}if(l===0&&e[p]){o="<span style='margin-left:"+e[p]+"em'/>"+o}g+=o}b(k).html(g)});return d};b.fn.flAutoKerning=function(d){return a.process(this,d)};delete c})(jQuery);
