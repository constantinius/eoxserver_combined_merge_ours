(function(){"use strict";var a=this;a.define(["backbone","communicator"],function(a,b){var c=a.Marionette.Controller.extend({initialize:function(){this._regionManager=new a.Marionette.RegionManager,b.reqres.setHandler("RM:addRegion",this.addRegion,this),b.reqres.setHandler("RM:removeRegion",this.removeRegion,this),b.reqres.setHandler("RM:getRegion",this.getRegion,this)},addRegion:function(a,b){return this._regionManager.addRegion(a,b)},removeRegion:function(a){this._regionManager.removeRegion(a)},getRegion:function(a){return this._regionManager.get(a)}});return new c})}).call(this);