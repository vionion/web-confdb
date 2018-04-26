var bigInt=(function(u){var R=10000000,H=7,X=9007199254740992,z=F(X),m=Math.log(X);function J(i,ae){if(typeof i==="undefined"){return J[0]}if(typeof ae!=="undefined"){return +ae===10?C(i):K(i,ae)}return C(i)}function g(ae,i){this.value=ae;this.sign=i;this.isSmall=false}g.prototype=Object.create(J.prototype);function E(i){this.value=i;this.sign=i<0;this.isSmall=true}E.prototype=Object.create(J.prototype);function b(i){return -X<i&&i<X}function F(i){if(i<10000000){return[i]}if(i<100000000000000){return[i%10000000,Math.floor(i/10000000)]}return[i%10000000,Math.floor(i/10000000)%10000000,Math.floor(i/100000000000000)]}function B(i){a(i);var ae=i.length;if(ae<4&&t(i,z)<0){switch(ae){case 0:return 0;case 1:return i[0];case 2:return i[0]+i[1]*R;default:return i[0]+(i[1]+i[2]*R)*R}}return i}function a(ae){var af=ae.length;while(ae[--af]===0){}ae.length=af+1}function V(ag){var ae=new Array(ag);var af=-1;while(++af<ag){ae[af]=0}return ae}function l(i){if(i>0){return Math.floor(i)}return Math.ceil(i)}function h(al,ak){var ah=al.length,ag=ak.length,ae=new Array(ah),am=0,af=R,aj,ai;for(ai=0;ai<ag;ai++){aj=al[ai]+ak[ai]+am;am=aj>=af?1:0;ae[ai]=aj-am*af}while(ai<ah){aj=al[ai]+am;am=aj===af?1:0;ae[ai++]=aj-am*af}if(am>0){ae.push(am)}return ae}function e(ae,i){if(ae.length>=i.length){return h(ae,i)}return h(i,ae)}function Y(af,ak){var ae=af.length,ai=new Array(ae),aj=R,ah,ag;for(ag=0;ag<ae;ag++){ah=af[ag]-aj+ak;ak=Math.floor(ah/aj);ai[ag]=ah-ak*aj;ak+=1}while(ak>0){ai[ag++]=ak%aj;ak=Math.floor(ak/aj)}return ai}g.prototype.add=function(af){var ag=C(af);if(this.sign!==ag.sign){return this.subtract(ag.negate())}var ae=this.value,i=ag.value;if(ag.isSmall){return new g(Y(ae,Math.abs(i)),this.sign)}return new g(e(ae,i),this.sign)};g.prototype.plus=g.prototype.add;E.prototype.add=function(af){var ag=C(af);var ae=this.value;if(ae<0!==ag.sign){return this.subtract(ag.negate())}var i=ag.value;if(ag.isSmall){if(b(ae+i)){return new E(ae+i)}i=F(Math.abs(i))}return new g(Y(i,Math.abs(ae)),ae<0)};E.prototype.plus=E.prototype.add;function o(am,al){var ah=am.length,aj=al.length,ae=new Array(ah),ak=0,af=R,ai,ag;for(ai=0;ai<aj;ai++){ag=am[ai]-ak-al[ai];if(ag<0){ag+=af;ak=1}else{ak=0}ae[ai]=ag}for(ai=aj;ai<ah;ai++){ag=am[ai]-ak;if(ag<0){ag+=af}else{ae[ai++]=ag;break}ae[ai]=ag}for(;ai<ah;ai++){ae[ai]=am[ai]}a(ae);return ae}function G(af,i,ae){var ag;if(t(af,i)>=0){ag=o(af,i)}else{ag=o(i,af);ae=!ae}ag=B(ag);if(typeof ag==="number"){if(ae){ag=-ag}return new E(ag)}return new g(ag,ae)}function q(al,ak,ag){var ai=al.length,ae=new Array(ai),am=-ak,af=R,aj,ah;for(aj=0;aj<ai;aj++){ah=al[aj]+am;am=Math.floor(ah/af);ah%=af;ae[aj]=ah<0?ah+af:ah}ae=B(ae);if(typeof ae==="number"){if(ag){ae=-ae}return new E(ae)}return new g(ae,ag)}g.prototype.subtract=function(af){var ag=C(af);if(this.sign!==ag.sign){return this.add(ag.negate())}var ae=this.value,i=ag.value;if(ag.isSmall){return q(ae,Math.abs(i),this.sign)}return G(ae,i,this.sign)};g.prototype.minus=g.prototype.subtract;E.prototype.subtract=function(af){var ag=C(af);var ae=this.value;if(ae<0!==ag.sign){return this.add(ag.negate())}var i=ag.value;if(ag.isSmall){return new E(ae-i)}return q(i,Math.abs(ae),ae>=0)};E.prototype.minus=E.prototype.subtract;g.prototype.negate=function(){return new g(this.value,!this.sign)};E.prototype.negate=function(){var i=this.sign;var ae=new E(-this.value);ae.sign=!i;return ae};g.prototype.abs=function(){return new g(this.value,false)};E.prototype.abs=function(){return new E(Math.abs(this.value))};function n(ao,an){var ah=ao.length,al=an.length,ag=ah+al,ae=V(ag),af=R,ap,aq,aj,ak,am;for(aj=0;aj<ah;++aj){ak=ao[aj];for(var ai=0;ai<al;++ai){am=an[ai];ap=ak*am+ae[aj+ai];aq=Math.floor(ap/af);ae[aj+ai]=ap-aq*af;ae[aj+ai+1]+=aq}}a(ae);return ae}function y(ag,ae){var af=ag.length,ai=new Array(af),ak=R,al=0,aj,ah;for(ah=0;ah<af;ah++){aj=ag[ah]*ae+al;al=Math.floor(aj/ak);ai[ah]=aj-al*ak}while(al>0){ai[ah++]=al%ak;al=Math.floor(al/ak)}return ai}function w(i,af){var ae=[];while(af-->0){ae.push(0)}return ae.concat(i)}function f(al,ai){var ae=Math.max(al.length,ai.length);if(ae<=30){return n(al,ai)}ae=Math.ceil(ae/2);var aj=al.slice(ae),ak=al.slice(0,ae),ag=ai.slice(ae),ah=ai.slice(0,ae);var an=f(ak,ah),af=f(aj,ag),i=f(e(ak,aj),e(ah,ag));var am=e(e(an,w(o(o(i,an),af),ae)),w(af,2*ae));a(am);return am}function c(ae,i){return -0.012*ae-0.012*i+0.000015*ae*i>0}g.prototype.multiply=function(ah){var ai=C(ah),ag=this.value,ae=ai.value,af=this.sign!==ai.sign,i;if(ai.isSmall){if(ae===0){return J[0]}if(ae===1){return this}if(ae===-1){return this.negate()}i=Math.abs(ae);if(i<R){return new g(y(ag,i),af)}ae=F(i)}if(c(ag.length,ae.length)){return new g(f(ag,ae),af)}return new g(n(ag,ae),af)};g.prototype.times=g.prototype.multiply;function A(af,i,ae){if(af<R){return new g(y(i,af),ae)}return new g(n(i,F(af)),ae)}E.prototype._multiplyBySmall=function(i){if(b(i.value*this.value)){return new E(i.value*this.value)}return A(Math.abs(i.value),F(Math.abs(this.value)),this.sign!==i.sign)};g.prototype._multiplyBySmall=function(i){if(i.value===0){return J[0]}if(i.value===1){return this}if(i.value===-1){return this.negate()}return A(Math.abs(i.value),this.value,this.sign!==i.sign)};E.prototype.multiply=function(i){return C(i)._multiplyBySmall(this)};E.prototype.times=E.prototype.multiply;function ac(al){var ag=al.length,ae=V(ag+ag),af=R,am,an,aj,ak,ai;for(aj=0;aj<ag;aj++){ak=al[aj];for(var ah=0;ah<ag;ah++){ai=al[ah];am=ak*ai+ae[aj+ah];an=Math.floor(am/af);ae[aj+ah]=am-an*af;ae[aj+ah+1]+=an}}a(ae);return ae}g.prototype.square=function(){return new g(ac(this.value),false)};E.prototype.square=function(){var i=this.value*this.value;if(b(i)){return new E(i)}return new g(ac(F(Math.abs(this.value))),false)};function P(ar,aq){var ak=ar.length,an=aq.length,af=R,av=V(aq.length),am=aq[an-1],ao=Math.ceil(af/(2*am)),at=y(ar,ao),ah=y(aq,ao),ai,ag,au,ap,al,aj,ae;if(at.length<=ak){at.push(0)}ah.push(0);am=ah[an-1];for(ag=ak-an;ag>=0;ag--){ai=af-1;if(at[ag+an]!==am){ai=Math.floor((at[ag+an]*af+at[ag+an-1])/am)}au=0;ap=0;aj=ah.length;for(al=0;al<aj;al++){au+=ai*ah[al];ae=Math.floor(au/af);ap+=at[ag+al]-(au-ae*af);au=ae;if(ap<0){at[ag+al]=ap+af;ap=-1}else{at[ag+al]=ap;ap=0}}while(ap!==0){ai-=1;au=0;for(al=0;al<aj;al++){au+=at[ag+al]-af+ah[al];if(au<0){at[ag+al]=au+af;au=0}else{at[ag+al]=au;au=1}}ap+=au}av[ag]=ai}at=k(at,ao)[0];return[B(av),B(at)]}function O(an,am){var ah=an.length,al=am.length,ao=[],af=[],ae=R,ai,ag,ak,aj,i;while(ah){af.unshift(an[--ah]);a(af);if(t(af,am)<0){ao.push(0);continue}ag=af.length;ak=af[ag-1]*ae+af[ag-2];aj=am[al-1]*ae+am[al-2];if(ag>al){ak=(ak+1)*ae}ai=Math.ceil(ak/aj);do{i=y(am,ai);if(t(i,af)<=0){break}ai--}while(ai);ao.push(ai);af=o(af,i)}ao.reverse();return[B(ao),B(af)]}function k(al,ak){var ah=al.length,ai=V(ah),af=R,aj,ae,am,ag;am=0;for(aj=ah-1;aj>=0;--aj){ag=am*af+al[aj];ae=l(ag/ak);am=ag-ae*ak;ai[aj]=ae|0}return[ai,am|0]}function W(ao,al){var ak,ae=C(al);var aj=ao.value,ai=ae.value;var af;if(ai===0){throw new Error("Cannot divide by zero")}if(ao.isSmall){if(ae.isSmall){return[new E(l(aj/ai)),new E(aj%ai)]}return[J[0],ao]}if(ae.isSmall){if(ai===1){return[ao,J[0]]}if(ai==-1){return[ao.negate(),J[0]]}var ap=Math.abs(ai);if(ap<R){ak=k(aj,ap);af=B(ak[0]);var an=ak[1];if(ao.sign){an=-an}if(typeof af==="number"){if(ao.sign!==ae.sign){af=-af}return[new E(af),new E(an)]}return[new g(af,ao.sign!==ae.sign),new E(an)]}ai=F(ap)}var am=t(aj,ai);if(am===-1){return[J[0],ao]}if(am===0){return[J[ao.sign===ae.sign?1:-1],J[0]]}if(aj.length+ai.length<=200){ak=P(aj,ai)}else{ak=O(aj,ai)}af=ak[0];var ah=ao.sign!==ae.sign,ag=ak[1],i=ao.sign;if(typeof af==="number"){if(ah){af=-af}af=new E(af)}else{af=new g(af,ah)}if(typeof ag==="number"){if(i){ag=-ag}ag=new E(ag)}else{ag=new g(ag,i)}return[af,ag]}g.prototype.divmod=function(ae){var i=W(this,ae);return{quotient:i[0],remainder:i[1]}};E.prototype.divmod=g.prototype.divmod;g.prototype.divide=function(i){return W(this,i)[0]};E.prototype.over=E.prototype.divide=g.prototype.over=g.prototype.divide;g.prototype.mod=function(i){return W(this,i)[1]};E.prototype.remainder=E.prototype.mod=g.prototype.remainder=g.prototype.mod;g.prototype.pow=function(ag){var aj=C(ag),af=this.value,ae=aj.value,ah,i,ai;if(ae===0){return J[1]}if(af===0){return J[0]}if(af===1){return J[1]}if(af===-1){return aj.isEven()?J[1]:J[-1]}if(aj.sign){return J[0]}if(!aj.isSmall){throw new Error("The exponent "+aj.toString()+" is too large.")}if(this.isSmall){if(b(ah=Math.pow(af,ae))){return new E(l(ah))}}i=this;ai=J[1];while(true){if(ae&1===1){ai=ai.times(i);--ae}if(ae===0){break}ae/=2;i=i.square()}return ai};E.prototype.pow=g.prototype.pow;g.prototype.modPow=function(ag,i){ag=C(ag);i=C(i);if(i.isZero()){throw new Error("Cannot take modPow with modulus 0")}var ae=J[1],af=this.mod(i);while(ag.isPositive()){if(af.isZero()){return J[0]}if(ag.isOdd()){ae=ae.multiply(af).mod(i)}ag=ag.divide(2);af=af.square().mod(i)}return ae};E.prototype.modPow=g.prototype.modPow;function t(af,ae){if(af.length!==ae.length){return af.length>ae.length?1:-1}for(var ag=af.length-1;ag>=0;ag--){if(af[ag]!==ae[ag]){return af[ag]>ae[ag]?1:-1}}return 0}g.prototype.compareAbs=function(af){var ag=C(af),ae=this.value,i=ag.value;if(ag.isSmall){return 1}return t(ae,i)};E.prototype.compareAbs=function(af){var ag=C(af),ae=Math.abs(this.value),i=ag.value;if(ag.isSmall){i=Math.abs(i);return ae===i?0:ae>i?1:-1}return -1};g.prototype.compare=function(af){if(af===Infinity){return -1}if(af===-Infinity){return 1}var ag=C(af),ae=this.value,i=ag.value;if(this.sign!==ag.sign){return ag.sign?1:-1}if(ag.isSmall){return this.sign?-1:1}return t(ae,i)*(this.sign?-1:1)};g.prototype.compareTo=g.prototype.compare;E.prototype.compare=function(af){if(af===Infinity){return -1}if(af===-Infinity){return 1}var ag=C(af),ae=this.value,i=ag.value;if(ag.isSmall){return ae==i?0:ae>i?1:-1}if(ae<0!==ag.sign){return ae<0?-1:1}return ae<0?1:-1};E.prototype.compareTo=E.prototype.compare;g.prototype.equals=function(i){return this.compare(i)===0};E.prototype.eq=E.prototype.equals=g.prototype.eq=g.prototype.equals;g.prototype.notEquals=function(i){return this.compare(i)!==0};E.prototype.neq=E.prototype.notEquals=g.prototype.neq=g.prototype.notEquals;g.prototype.greater=function(i){return this.compare(i)>0};E.prototype.gt=E.prototype.greater=g.prototype.gt=g.prototype.greater;g.prototype.lesser=function(i){return this.compare(i)<0};E.prototype.lt=E.prototype.lesser=g.prototype.lt=g.prototype.lesser;g.prototype.greaterOrEquals=function(i){return this.compare(i)>=0};E.prototype.geq=E.prototype.greaterOrEquals=g.prototype.geq=g.prototype.greaterOrEquals;g.prototype.lesserOrEquals=function(i){return this.compare(i)<=0};E.prototype.leq=E.prototype.lesserOrEquals=g.prototype.leq=g.prototype.lesserOrEquals;g.prototype.isEven=function(){return(this.value[0]&1)===0};E.prototype.isEven=function(){return(this.value&1)===0};g.prototype.isOdd=function(){return(this.value[0]&1)===1};E.prototype.isOdd=function(){return(this.value&1)===1};g.prototype.isPositive=function(){return !this.sign};E.prototype.isPositive=function(){return this.value>0};g.prototype.isNegative=function(){return this.sign};E.prototype.isNegative=function(){return this.value<0};g.prototype.isUnit=function(){return false};E.prototype.isUnit=function(){return Math.abs(this.value)===1};g.prototype.isZero=function(){return false};E.prototype.isZero=function(){return this.value===0};g.prototype.isDivisibleBy=function(i){var af=C(i);var ae=af.value;if(ae===0){return false}if(ae===1){return true}if(ae===2){return this.isEven()}return this.mod(af).equals(J[0])};E.prototype.isDivisibleBy=g.prototype.isDivisibleBy;function x(i){var ae=i.abs();if(ae.isUnit()){return false}if(ae.equals(2)||ae.equals(3)||ae.equals(5)){return true}if(ae.isEven()||ae.isDivisibleBy(3)||ae.isDivisibleBy(5)){return false}if(ae.lesser(25)){return true}}g.prototype.isPrime=function(){var al=x(this);if(al!==u){return al}var af=this.abs(),ae=af.prev();var ak=[2,3,5,7,11,13,17,19],ai=ae,ah,am,ag,aj;while(ai.isEven()){ai=ai.divide(2)}for(ag=0;ag<ak.length;ag++){aj=bigInt(ak[ag]).modPow(ai,af);if(aj.equals(J[1])||aj.equals(ae)){continue}for(am=true,ah=ai;am&&ah.lesser(ae);ah=ah.multiply(2)){aj=aj.square().mod(af);if(aj.equals(ae)){am=false}}if(am){return false}}return true};E.prototype.isPrime=g.prototype.isPrime;g.prototype.isProbablePrime=function(ai){var ah=x(this);if(ah!==u){return ah}var aj=this.abs();var ag=ai===u?5:ai;for(var af=0;af<ag;af++){var ae=bigInt.randBetween(2,aj.minus(2));if(!ae.modPow(aj.prev(),aj).isUnit()){return false}}return true};E.prototype.isProbablePrime=g.prototype.isProbablePrime;g.prototype.modInv=function(ak){var ah=bigInt.zero,af=bigInt.one,ai=C(ak),ag=this.abs(),aj,i,ae;while(!ag.equals(bigInt.zero)){aj=ai.divide(ag);i=ah;ae=ai;ah=af;ai=ag;af=i.subtract(aj.multiply(af));ag=ae.subtract(aj.multiply(ag))}if(!ai.equals(1)){throw new Error(this.toString()+" and "+ak.toString()+" are not co-prime")}if(ah.compare(0)===-1){ah=ah.add(ak)}if(this.isNegative()){return ah.negate()}return ah};E.prototype.modInv=g.prototype.modInv;g.prototype.next=function(){var i=this.value;if(this.sign){return q(i,1,this.sign)}return new g(Y(i,1),this.sign)};E.prototype.next=function(){var i=this.value;if(i+1<X){return new E(i+1)}return new g(z,false)};g.prototype.prev=function(){var i=this.value;if(this.sign){return new g(Y(i,1),true)}return q(i,1,this.sign)};E.prototype.prev=function(){var i=this.value;if(i-1>-X){return new E(i-1)}return new g(z,true)};var N=[1];while(2*N[N.length-1]<=R){N.push(2*N[N.length-1])}var U=N.length,L=N[U-1];function I(i){return((typeof i==="number"||typeof i==="string")&&+Math.abs(i)<=R)||(i instanceof g&&i.value.length<=1)}g.prototype.shiftLeft=function(ae){if(!I(ae)){throw new Error(String(ae)+" is too large for shifting.")}ae=+ae;if(ae<0){return this.shiftRight(-ae)}var i=this;while(ae>=U){i=i.multiply(L);ae-=U-1}return i.multiply(N[ae])};E.prototype.shiftLeft=g.prototype.shiftLeft;g.prototype.shiftRight=function(af){var ae;if(!I(af)){throw new Error(String(af)+" is too large for shifting.")}af=+af;if(af<0){return this.shiftLeft(-af)}var i=this;while(af>=U){if(i.isZero()){return i}ae=W(i,L);i=ae[1].isNegative()?ae[0].prev():ae[0];af-=U-1}ae=W(i,N[af]);return ae[1].isNegative()?ae[0].prev():ae[0]};E.prototype.shiftRight=g.prototype.shiftRight;function S(aq,an,ao){an=C(an);var af=aq.isNegative(),ae=an.isNegative();var am=af?aq.not():aq,ai=ae?an.not():an;var ah=0,al=0;var ap=null,ag=null;var ar=[];while(!am.isZero()||!ai.isZero()){ap=W(am,L);ah=ap[1].toJSNumber();if(af){ah=L-1-ah}ag=W(ai,L);al=ag[1].toJSNumber();if(ae){al=L-1-al}am=ap[0];ai=ag[0];ar.push(ao(ah,al))}var ak=ao(af?1:0,ae?1:0)!==0?bigInt(-1):bigInt(0);for(var aj=ar.length-1;aj>=0;aj-=1){ak=ak.multiply(L).add(bigInt(ar[aj]))}return ak}g.prototype.not=function(){return this.negate().prev()};E.prototype.not=g.prototype.not;g.prototype.and=function(i){return S(this,i,function(af,ae){return af&ae})};E.prototype.and=g.prototype.and;g.prototype.or=function(i){return S(this,i,function(af,ae){return af|ae})};E.prototype.or=g.prototype.or;g.prototype.xor=function(i){return S(this,i,function(af,ae){return af^ae})};E.prototype.xor=g.prototype.xor;var v=1<<30,j=(R&-R)*(R&-R)|v;function T(af){var ae=af.value,i=typeof ae==="number"?ae|v:ae[0]+ae[1]*R|j;return i&-i}function D(ae,i){ae=C(ae);i=C(i);return ae.greater(i)?ae:i}function ab(ae,i){ae=C(ae);i=C(i);return ae.lesser(i)?ae:i}function M(ae,i){ae=C(ae).abs();i=C(i).abs();if(ae.equals(i)){return ae}if(ae.isZero()){return i}if(i.isZero()){return ae}var ah=J[1],ag,af;while(ae.isEven()&&i.isEven()){ag=Math.min(T(ae),T(i));ae=ae.divide(ag);i=i.divide(ag);ah=ah.multiply(ag)}while(ae.isEven()){ae=ae.divide(T(ae))}do{while(i.isEven()){i=i.divide(T(i))}if(ae.greater(i)){af=i;i=ae;ae=af}i=i.subtract(ae)}while(!i.isZero());return ah.isUnit()?ae:ae.multiply(ah)}function d(ae,i){ae=C(ae).abs();i=C(i).abs();return ae.divide(M(ae,i)).multiply(i)}function p(an,am){an=C(an);am=C(am);var aj=ab(an,am),af=D(an,am);var ah=af.subtract(aj).add(1);if(ah.isSmall){return aj.add(Math.floor(Math.random()*ah))}var ae=ah.value.length-1;var ao=[],ai=true;for(var ag=ae;ag>=0;ag--){var al=ai?ah.value[ag]:R;var ak=l(Math.random()*al);ao.unshift(ak);if(ak<al){ai=false}}ao=B(ao);return aj.add(typeof ao==="number"?new E(ao):new g(ao,false))}var K=function(an,ag){var ai=an.length;var ak;var aj=Math.abs(ag);for(var ak=0;ak<ai;ak++){var al=an[ak].toLowerCase();if(al==="-"){continue}if(/[a-z0-9]/.test(al)){if(/[0-9]/.test(al)&&+al>=aj){if(al==="1"&&aj===1){continue}throw new Error(al+" is not a valid digit in base "+ag+".")}else{if(al.charCodeAt(0)-87>=aj){throw new Error(al+" is not a valid digit in base "+ag+".")}}}}if(2<=ag&&ag<=36){if(ai<=m/Math.log(ag)){var ao=parseInt(an,ag);if(isNaN(ao)){throw new Error(al+" is not a valid digit in base "+ag+".")}return new E(parseInt(an,ag))}}ag=C(ag);var ah=[];var ae=an[0]==="-";for(ak=ae?1:0;ak<an.length;ak++){var al=an[ak].toLowerCase(),am=al.charCodeAt(0);if(48<=am&&am<=57){ah.push(C(al))}else{if(97<=am&&am<=122){ah.push(C(al.charCodeAt(0)-87))}else{if(al==="<"){var af=ak;do{ak++}while(an[ak]!==">");ah.push(C(an.slice(af+1,ak)))}else{throw new Error(al+" is not a valid character")}}}}return aa(ah,ag,ae)};function aa(ai,ah,ae){var aj=J[0],ag=J[1],af;for(af=ai.length-1;af>=0;af--){aj=aj.add(ai[af].times(ag));ag=ag.times(ah)}return ae?aj.negate():aj}function ad(ae){var i=ae.value;if(typeof i==="number"){i=[i]}if(i.length===1&&i[0]<=35){return"0123456789abcdefghijklmnopqrstuvwxyz".charAt(i[0])}return"<"+i+">"}function Q(aj,ag){ag=bigInt(ag);if(ag.isZero()){if(aj.isZero()){return"0"}throw new Error("Cannot convert nonzero numbers to base 0.")}if(ag.equals(-1)){if(aj.isZero()){return"0"}if(aj.isNegative()){return new Array(1-aj).join("10")}return"1"+new Array(+aj).join("01")}var i="";if(aj.isNegative()&&ag.isPositive()){i="-";aj=aj.abs()}if(ag.equals(1)){if(aj.isZero()){return"0"}return i+new Array(+aj+1).join(1)}var ae=[];var ah=aj,af;while(ah.isNegative()||ah.compareAbs(ag)>=0){af=ah.divmod(ag);ah=af.quotient;var ai=af.remainder;if(ai.isNegative()){ai=ag.minus(ai).abs();ah=ah.next()}ae.push(ad(ai))}ae.push(ad(ah));return i+ae.reverse().join("")}g.prototype.toString=function(ah){if(ah===u){ah=10}if(ah!==10){return Q(this,ah)}var ag=this.value,ae=ag.length,ai=String(ag[--ae]),af="0000000",aj;while(--ae>=0){aj=String(ag[ae]);ai+=af.slice(aj.length)+aj}var i=this.sign?"-":"";return i+ai};E.prototype.toString=function(i){if(i===u){i=10}if(i!=10){return Q(this,i)}return String(this.value)};g.prototype.toJSON=E.prototype.toJSON=function(){return this.toString()};g.prototype.valueOf=function(){return +this.toString()};g.prototype.toJSNumber=g.prototype.valueOf;E.prototype.valueOf=function(){return this.value};E.prototype.toJSNumber=E.prototype.valueOf;function s(am){if(b(+am)){var al=+am;if(al===l(al)){return new E(al)}throw"Invalid integer: "+am}var ae=am[0]==="-";if(ae){am=am.slice(1)}var aj=am.split(/e/i);if(aj.length>2){throw new Error("Invalid integer: "+aj.join("e"))}if(aj.length===2){var ag=aj[1];if(ag[0]==="+"){ag=ag.slice(1)}ag=+ag;if(ag!==l(ag)||!b(ag)){throw new Error("Invalid integer: "+ag+" is not a valid exponent.")}var an=aj[0];var ai=an.indexOf(".");if(ai>=0){ag-=an.length-ai-1;an=an.slice(0,ai)+an.slice(ai+1)}if(ag<0){throw new Error("Cannot include negative exponent part for integers")}an+=(new Array(ag+1)).join("0");am=an}var ao=/^([0-9][0-9]*)$/.test(am);if(!ao){throw new Error("Invalid integer: "+am)}var i=[],ak=am.length,af=H,ah=ak-af;while(ak>0){i.push(+am.slice(ah,ak));ah-=af;if(ah<0){ah=0}ak-=af}a(i);return new g(i,ae)}function r(i){if(b(i)){if(i!==l(i)){throw new Error(i+" is not an integer.")}return new E(i)}return s(i.toString())}function C(i){if(typeof i==="number"){return r(i)}if(typeof i==="string"){return s(i)}return i}for(var Z=0;Z<1000;Z++){J[Z]=new E(Z);if(Z>0){J[-Z]=new E(-Z)}}J.one=J[1];J.zero=J[0];J.minusOne=J[-1];J.max=D;J.min=ab;J.gcd=M;J.lcm=d;J.isInstance=function(i){return i instanceof g||i instanceof E};J.randBetween=p;J.fromArray=function(af,ae,i){return aa(af.map(C),C(ae||10),i)};return J})();if(typeof module!=="undefined"&&module.hasOwnProperty("exports")){module.exports=bigInt}if(typeof define==="function"&&define.amd){define("big-integer",[],function(){return bigInt})};