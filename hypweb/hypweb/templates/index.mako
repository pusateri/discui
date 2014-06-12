<%inherit file="/base.mako" />

<%def name="head_extra()">
<link rel="stylesheet" href="${request.static_url('hypweb:static/style/ui.jqgrid.css')}" type="text/css" media="screen" charset="utf-8" />
<script src="${request.static_url('hypweb:static/scripts/grid.locale-en.js')}" type="text/javascript"></script>
<script src="${request.static_url('hypweb:static/scripts/jquery.jqGrid.min.js')}" type="text/javascript"></script>
</%def>
<%def name="nav_section()">summary</%def>

	<table id="summary"></table>
	<div id="pager"></div>
	<script type="text/javascript">
	$("#summary").jqGrid({
		url:'${summary_url}',
		datatype: "json",
		height: 'auto',
	   	colModel:[
			{name:'order',label:'Order', width:20, align:"right", sorttype:"int", hidden:true},	
	   		{name:'name',label:'Name', width:300},
	   		{name:'value',label:'Value', width:550},
	   	],
		pager:"#pager",
		pgbuttons:false,
		pginput:false,
		sortname: "order",
		sortorder: "desc",
		caption: "System Summary",
		loadonce:true,
	}).navGrid("#pager",{add:false,edit:false,del:false,view:false,search:true,searchtitle:"Search for System Properties",refresh:false});
	
	</script>

