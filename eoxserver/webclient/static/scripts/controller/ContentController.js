(function(){"use strict";var a=this;a.require(["backbone","communicator","app"],function(a,b,c){var d=a.Marionette.Controller.extend({initialize:function(){this.listenTo(b.mediator,"dialog:open:about",this.onDialogOpenAbout),this.listenTo(b.mediator,"ui:open:layercontrol",this.onLayerControlOpen),this.listenTo(b.mediator,"ui:open:toolselection",this.onToolSelectionOpen)},onDialogOpenAbout:function(){c.dialogRegion.show(c.DialogContentView)},onLayerControlOpen:function(){_.isUndefined(c.layout.isClosed)||c.layout.isClosed?(c.leftSideBar.show(c.layout),c.layout.baseLayers.show(c.baseLayerView),c.layout.products.show(c.productsView),c.layout.overlays.show(c.overlaysView)):c.layout.close()},onToolSelectionOpen:function(){_.isUndefined(c.toolLayout.isClosed)||c.toolLayout.isClosed?(c.rightSideBar.show(c.toolLayout),c.toolLayout.selection.show(c.selectionToolsView),c.toolLayout.visualization.show(c.visualizationToolsView)):c.toolLayout.close()}});return new d})}).call(this);