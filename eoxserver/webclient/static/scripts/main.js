(function(){"use strict";function a(a){a&&"undefined"!=typeof console&&console.log||(window.console={debug:function(){},trace:function(){},log:function(){},info:function(){},warn:function(){},error:function(){}})}var b=this;b.require(["backbone","app","backbone.marionette","regionManager","jquery","jqueryui","text!config.json","util","libcoverage"],function(c,d){$.getJSON("configuration/",function(c){a(c.debug);var e=[],f=[],g=[];_.each(c.views,function(a){e.push(a)},this),_.each(c.models,function(a){f.push(a)},this),_.each(c.templates,function(a){g.push(a.template)},this),b.require([].concat(c.mapConfig.visualizationLibs,c.mapConfig.module,c.mapConfig.model,e,f,g),function(){d.configure(c),d.start()}),setTimeout(function(){$("#loadscreen").length&&($("#loadscreen").remove(),$("#error-messages").append('<div class="alert alert-warning alert-danger"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><strong>Warning!</strong> <p>There was a problem loading the application, some functionality might not be available.</p><p>Please contact the website administrator if you have any problems.</p></div>'))},1e4)}).fail(function(){$("#loadscreen").empty(),$("#loadscreen").html('<p class="warninglabel">There was a problem loading the configuration file, please contact the site administrator</p>')})})}).call(this);