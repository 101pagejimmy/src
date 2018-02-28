function openCancelDialog(node, cancel_url, delete_url, event){
  event.stopPropagation();
  var btns = {"This":function(){window.location=cancel_url;}, "All":function(){window.location=delete_url}, "Do nothing":function(){$(this).dialog("destroy");}};
  var dia = $("#delete_dialog").dialog({'buttons':btns, 'modal':true});
  dia.dialog('open');
  return false;
}

function openEditDialog(event, node, occurrence_url, event_url){
  event.stopPropagation();
  var btns = {"This":function(){window.location=occurrence_url;}, "All":function(){window.location=event_url}, "Do nothing":function(){$(this).dialog("destroy");}};
  var dia = $("#edit_dialog").dialog({'buttons': btns, 'modal': true});
  dia.dialog('open');
  return false;
}

function openDetail(event, node){
  event.stopPropagation();
  var btns = { "Close":function(){$(this).dialog("destroy");}};
  var dia = $($(node).attr("href")).dialog({'buttons':btns, 'modal':true, 'title':'Details'});
  dia.dialog('open');
  return false;
}

function openURL(url, event){
    event.stopPropagation();
    window.location=url;
}