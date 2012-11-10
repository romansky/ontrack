var Items = Backbone.Collection.extend({
	trackID: null,
	model: Item,
	url: function(){	
		//return "http://192.168.100.136/api/track/" + this.trackID
		return "item.php";
	},
	initialize: function(models,options){
		this.trackID = options.trackID;
	}
});