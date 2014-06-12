<%inherit file="/base.mako" />

<%def name="head_extra()">
<link rel="stylesheet" href="${request.static_url('hypweb:static/style/ui.jqgrid.css')}" type="text/css" media="screen" charset="utf-8" />
<script src="${request.static_url('hypweb:static/scripts/grid.locale-en.js')}" type="text/javascript"></script>
<script src="${request.static_url('hypweb:static/scripts/jquery.jqGrid.min.js')}" type="text/javascript"></script>
</%def>
<%def name="nav_section()">debug</%def>

	<table id="debug"></table>
	<div id="pager1"></div>
	<table id="stats"></table>
	<div id="pager2"></div>
	<table id="hosts"></table>
	<div id="pager3"></div>
	<script type="text/javascript">
	$("#debug").jqGrid({
		url:'${debug_url}',
		datatype: "json",
		height: 'auto',
	   	colModel:[
			{name:'type',label:'Type', width:200},	
	   		{name:'size',label:'Size', width:100, sorttype:"int"},
	   		{name:'alloced',label:'Allocated', width:100, sorttype:"int"},
			{name:'freed',label:'Freed', width:100, sorttype:"int"},
			{name:'inuse',label:'In use', width:100, sorttype:"int"},
			{name:'bytes',label:'Bytes', width:100, sorttype:"int"},
	   	],
		pager:"#pager1",
		pgbuttons:false,
		pginput:false,
		sortname: "size",
		sortorder: "desc",
		caption: "Memory Usage",
		loadonce:true,
	}).navGrid("#pager1",{add:false,edit:false,del:false,view:false,search:true,searchtitle:"Search for Memory Properties",refresh:false});
	
	$("#stats").jqGrid({
		url:'${stats_url}',
		datatype: "json",
		height: 'auto',
	   	colModel:[
			{name:'key',label:'Value', width:200, sorttype:"int"},	
	   	],
		pager:"#pager2",
		pgbuttons:false,
		pginput:false,
		sortname: "Key",
		sortorder: "desc",
		caption: "Statistics",
		loadonce:true,
	}).navGrid("#pager2",{add:false,edit:false,del:false,view:false,search:true,searchtitle:"Search for Host Properties",refresh:false});
	$("#hosts").jqGrid({
		url:'${hosts_url}',
		datatype: "json",
		height: 'auto',
	   	colModel:[
			{name:'address',label:'Address', width:200},	
	   		{name:'query_sent',label:'Queries Sent', width:100, sorttype:"int"},
	   		{name:'query_received',label:'Queries Rcvd', width:100, sorttype:"int"},
	   		{name:'response_sent',label:'Responses Sent', width:120, sorttype:"int"},
	   		{name:'response_received',label:'Responses Rcvd', width:120, sorttype:"int"},
	   	],
		pager:"#pager3",
		pgbuttons:false,
		pginput:false,
		sortname: "address",
		sortorder: "desc",
		caption: "Send/Receive hosts",
		loadonce:true,
	}).navGrid("#pager3",{add:false,edit:false,del:false,view:false,search:true,searchtitle:"Search for Host Properties",refresh:false});
	
	</script>

