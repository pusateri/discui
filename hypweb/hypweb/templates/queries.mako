<%inherit file="/base.mako" />

<%def name="head_extra()">
<link rel="stylesheet" href="${request.static_url('hypweb:static/style/ui.jqgrid.css')}" type="text/css" media="screen" charset="utf-8" />
<script src="${request.static_url('hypweb:static/scripts/grid.locale-en.js')}" type="text/javascript"></script>
<script src="${request.static_url('hypweb:static/scripts/jquery.jqGrid.min.js')}" type="text/javascript"></script>
</%def>
<%def name="nav_section()">queries</%def>

	<table id="queries"></table>
	<div id="pager"></div>
	<script type="text/javascript">
	String.prototype.format = function () {
	  var args = arguments;
	  return this.replace(/\{(\d+)\}/g, function (m, n) { return args[n]; });
	};
	function showSeconds (val, cellProps, rowData) {
		var minutes = 0;
		var seconds = val;
		if (seconds > 60) {
			minutes = Math.floor(seconds / 60);
			seconds = seconds % 60;
		}
		if (minutes) {
			return "{0} minutes, {1} seconds".format(minutes, seconds);
		} else {
			return "{0} seconds".format(seconds);
		}
	}
	$("#queries").jqGrid({
		data: ${queries|n},
		datatype: "local",
		height: 'auto',
	   	colModel:[
			{name:'active',label:'Time Active', width:200, formatter: showSeconds},
			{name:'service',label:'Service', width:150},
            {name:'type',label:"Query Type", width:100},
	   		{name:'ifName',label:'Interface Name', width:150},
			{name:'ifIndex',label:'Interface Index', width:100},
			{name:'uuid',label:'UUID', width:300},
	   	],
		pager:"#pager",
		pgbuttons:false,
		pginput:false,
		sortname: "active",
		sortorder: "desc",
		caption: "Pending Queries",
		loadonce:true,
	}).navGrid("#pager",{add:false,edit:false,del:false,view:false,search:true,searchtitle:"Search for Service",refresh:false});
	
	</script>

