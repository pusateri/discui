<%inherit file="/base.mako" />

<%def name="head_extra()">
<link rel="stylesheet" href="${request.static_url('hypweb:static/style/ui.jqgrid.css')}" type="text/css" media="screen" charset="utf-8" />
<script src="${request.static_url('hypweb:static/scripts/grid.locale-en.js')}" type="text/javascript"></script>
<script src="${request.static_url('hypweb:static/scripts/jquery.jqGrid.min.js')}" type="text/javascript"></script>
</%def>
<%def name="nav_section()">services</%def>
    <table id="srv"></table>
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
    $("#srv").jqGrid({
        data: ${services|n},
        datatype: "local",
        height: 'auto',
        colModel:[
            {name:'service',label:'Service', width:330},
            {name:'instance',label:'Instance', width:330, ignoreCase:true},
            {name:'rrtype',label:'Record Type', width:80, align:"center"},
            {name:'ttl',label:'Time To Live', width:80, align:"right",sorttype:"integer"},
            {name:'rdata',label:'Record Data', width:400},
        ],
        pager:"#pager",
        pgbuttons:true,
        pginput:true,
        viewrecords:true,
        rowNum:50,
        recordtext:"Showing [{0}-{1}] of {2}",
        sortname: "name",
        sortorder: "desc",
        caption: "Active Cache Entries",
        loadonce:true,
    }).navGrid("#pager",{add:false,edit:false,del:false,view:false,search:true,searchtitle:"Search for Service",refresh:false});
    
    </script>

