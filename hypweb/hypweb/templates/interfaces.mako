<%inherit file="/base.mako" />

<%def name="head_extra()">
<link rel="stylesheet" href="${request.static_url('hypweb:static/style/ui.jqgrid.css')}" type="text/css" media="screen" charset="utf-8" />
<script src="${request.static_url('hypweb:static/scripts/grid.locale-en.js')}" type="text/javascript"></script>
<script src="${request.static_url('hypweb:static/scripts/jquery.jqGrid.min.js')}" type="text/javascript"></script>
</%def>
<%def name="nav_section()">interfaces</%def>

% for instance in instances:
	<table id="list${instance['index']}"></table>
	<div id="pager"></div>
	<script type="text/javascript">
	function showVersion (val, cellProps, rowData) {
	    if (val == 4) {
	        return "v4";
	    } else if (val == 6){
	        return "v6";
	    } else {
	    	return "Unknown";
	    }
	}
	function myLinkFormatter (cellvalue, options, rowObject) {
	    return '<a href = "/services/' + rowObject.index + '"> ' + rowObject.ncache + '</a>';
	}
	$("#list${instance['index']}").jqGrid({
		url:'${instances_url}${instance['index']}/interfaces/',
		datatype: "json",
		height: 'auto',
	   	colModel:[
	   		{name:'name',label:'Name', width:60},
	   		{name:'index',label:'IfIndex', width:50, align:"right", sorttype:"int"},
	   		{name:'family',label:'Family', width:50, align:"center", formatter: showVersion},
	   		{name:'prefix',label:'Prefix', width:120},
	   		{name:'address',label:'Address', width:160},		
	   		{name:'flags',label:'Flags', width:150, sortable:false},
			{name:'subdomain',label:'Subdomain Name', width:140, editable:true,
				editoptions:{
					placeholder:"Enter name published in DNS"
				}
			},
			{name:'dnsname',label:'Reverse DNS Name', width:180},
			{name:'ncache',label:'# Cache', width:80, align:"right", formatter:myLinkFormatter},
	   	],
	   	autowidth: false,
		pager:"#pager",
		pgbuttons:false,
		pginput:false,
		sortname: "name",
		sortorder: "desc",
		caption: "Instance: ${instance['name']}",
		loadonce:true,
	}).navGrid("#pager",{add:false,edit:true,edittitle:"Edit DNS Name",del:false,view:false,search:true,searchtitle:"Search for Interface properties",refresh:false});
	
	</script>
% endfor
