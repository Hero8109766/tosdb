/*!
 * Lunr languages, `Korean` language
 * https://github.com/MihaiValentin/lunr-languages
 *
 * Copyright 2014, Chad Liu
 * http://www.mozilla.org/MPL/
 */
/*!
 * based on
 * Snowball JavaScript Library v0.3
 * http://code.google.com/p/urim/
 * http://snowball.tartarus.org/
 *
 * Copyright 2010, Oleg Mazko
 * http://www.mozilla.org/MPL/
 */

/**
 * export the module via AMD, CommonJS or as a browser global
 * Export code from https://github.com/umdjs/umd/blob/master/returnExports.js
 */
;
(function(root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(factory)
    } else if (typeof exports === 'object') {
        /**
         * Node. Does not work with strict CommonJS, but
         * only CommonJS-like environments that support module.exports,
         * like Node.
         */
        module.exports = factory()
    } else {
        // Browser globals (root is window)
        factory()(root.lunr);
    }
}(this, function() {
    /**
     * Just return a value to define the module export.
     * This example returns an object, but the module
     * can return a function as the exported value.
     */
    return function(lunr) {
        /* throw error if lunr is not yet included */
        if ('undefined' === typeof lunr) {
            throw new Error('Lunr is not present. Please include / require Lunr before this script.');
        }

        /* throw error if lunr stemmer support is not yet included */
        if ('undefined' === typeof lunr.stemmerSupport) {
            throw new Error('Lunr stemmer support is not present. Please include / require Lunr stemmer support before this script.');
        }

        /*
        Korean tokenization is trickier, since it does not
        take into account spaces.
        Since the tokenization function is represented different
        internally for each of the Lunr versions, this had to be done
        in order to try to try to pick the best way of doing this based
        on the Lunr version
         */
        var isLunr2 = lunr.version[0] == "2";

        /* register specific locale function */
        lunr.ch = function() {
            this.pipeline.reset();
            this.pipeline.add(
                lunr.ch.stopWordFilter,
                lunr.ch.stemmer
            );

            // change the tokenizer for korean one
            if (isLunr2) { // for lunr version 2.0.0
                this.tokenizer = lunr.ch.tokenizer;
            } else {
                if (lunr.tokenizer) { // for lunr version 0.6.0
                    lunr.tokenizer = lunr.ch.tokenizer;
                }
                if (this.tokenizerFn) { // for lunr version 0.7.0 -> 1.0.0
                    this.tokenizerFn = lunr.ch.tokenizer;
                }
            }
        };

        lunr.ch.tokenizer = function (obj) {
            throw new Error('To be implemented');
        };

        /* lunr stemmer function */
        lunr.ch.stemmer = (function() {

            /* TODO chinese stemmer  */
            return function(word) {
                return word;
            }
        })();

        lunr.Pipeline.registerFunction(lunr.ch.stemmer, 'stemmer-ch');
        lunr.ch.wordCharacters = "[\u4E00-\u9FCC\u3400-\u4DB5\uFA0E\uFA0F\uFA11\uFA13\uFA14\uFA1F\uFA21\uFA23\uFA24\uFA27-\uFA29]|[\ud840-\ud868][\udc00-\udfff]|\ud869[\udc00-\uded6\udf00-\udfff]|[\ud86a-\ud86c][\udc00-\udfff]|\ud86d[\udc00-\udf34\udf40-\udfff]|\ud86e[\udc00-\udc1d]";

        /* stop word filter function */
        lunr.ch.stopWordFilter = function(token) {
            if (lunr.ch.stopWordFilter.stopWords.indexOf(isLunr2 ? token.toString() : token) === -1) {
                return token;
            }
        };

        // stopword for korean is from http://www.ranks.nl/stopwords/korean
        lunr.ch.stopWordFilter = lunr.generateStopWordFilter(
            [' ', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???']
        );

        lunr.Pipeline.registerFunction(lunr.ch.stopWordFilter, 'stopWordFilter-ch');
    };
}));
