(function($, undefined){
  $.widget("ui.checkbox", {
    options:
    {
      divClass : "checkbox"
    },
    _create: function()
    {
      var self = this;
      var div = $("<div class=\""+self.options.divClass+"\">&nbsp;</div>");
      
      if( self.element.is(':checked') )
        div.addClass( "checked" )
      
      if( self.element.attr("disabled") )
        div.addClass("disabled")
        

      // Пре стилизация
      div.css({"width":self.element.outerWidth()+"px", "height":self.element.outerHeight()+"px" });
      
      
      // Чисто для форума
      if( self.element.attr("rel") !="" )
        div.css({"background-color": self.element.attr("rel") })
      
      // Добавление
      div.insertAfter( self.element );

      div.bind("click",function(e){
        if( $(this).hasClass("disabled") )
          return;
        self.element.trigger("click");
        e.preventDefault()
      })
      
      self.element.bind("change", function(e){
        if( self.element.is(':checked') )
          div.addClass( "checked" )
        else
          div.removeClass( "checked" )
        if( self.element.attr("disabled") )
          div.addClass("disabled")
        else
          div.removeClass("disabled")
        e.preventDefault();
      })

      self.div = div;
      self.element.hide();
    },
    destroy: function()
    {
      var self = this;
      
      self.element.show();
      self.element.unbind("change");
      self.div.remove()
      
      $.Widget.prototype.destroy.call( this );
    },
    
    disable: function()
    {
      var self = this;
      self.div.addClass("disabled");
      self.element.attr("disabled", "disabled");
    },
    
    enable: function()
    {
      var self = this;
      self.div.removeClass("disabled");
      self.element.removeAttr("disabled");
      
    },
            
    removeChecked: function()
    {
      var self = this;
      self.div.removeClass("checked");
      self.element.removeAttr("checked");
    }        
    
    
    
  });
})(jQuery)