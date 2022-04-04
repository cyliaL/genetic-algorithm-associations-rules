var capacite = 0 ; 
var items = [] ; 
var nombre_items = 0 ; 
var solution = [] ; 


/*---------------------------------------------------------------------------------------------*/
        
        async function loadFile(file) {
            let text = await (new Response(file)).text();
            var list= text.split('\n') ;
            var list = list.map(function (x) { return parseInt(x); });
            capacite =  list[1]  ; 
            nombre_items = list[0] ; 
            items = list.slice(2 , list[0]+2 ) ;
            var objets = $(".body_objets")[0] ; 
            var nb = $("#NB")[0] ; 
            var c = $("#capacite")[0] ; 
            var poids = $("#Poids")[0] ; 
        
            poids.innerHTML = Math.min (...items) + " < p < " + Math.max (...items) ; 
            c.innerHTML = capacite ; 
            nb.innerHTML = nombre_items ; 
            for(var i = 0 ; i <items.length ; i++) {
                var tr = document.createElement('tr') ; 
                tr.innerHTML=" <td> " +i + " </td> <td> " + items[i]+ "</td>" ; 
                objets.append (tr) ; 
            }
         
            document.getElementById("sol_bins1").innerHTML = "" ; 
            document.getElementById("time1").innerHTML ="" ; 
            document.getElementById("sol_bins2").innerHTML = "" ; 
            document.getElementById("time2").innerHTML ="" ; 
        
        }
        //just for test
        async function run() {
            var tab =[];
            tab  = await eel.ffd_py(capacite,items)();
            var a = tab[0];
            var b = tab[1];
            var c = [];
            c = tab[2];
            console.log(a + " from Python")
            console.log(b + " from Python")
            console.log(c + " from Python")
         }
         
       
         async function loadtable(tab){
            //-------------------
			var set =  new Set(tab[2])   ;
            var p = 0 ; 
			var list_bins  = Array.from(set);
            var weights = new Array(list_bins.length); 

            weights.fill(0) ;
            var affectation = new Array( tab[0]) ; 
            for(var k = 0 ; k< tab[0] ; k++ ) {
                affectation[k] = [] ;  
            }
            for ( var i= 0 ; i < affectation.length ; i++ ) {
                for(var j = 0 ; j< tab[2].length; j++) {
                    if(tab[2][j]==list_bins[i]) {
                        affectation[i].push(j) ; 
                        weights[i] += items[j] ; 
                    }
                } 
                    }
                    console.log(weights) ; 
                    var aff = $('.affectation')[0] ; 
                    for(i = 0 ; i<affectation.length ; i++ ) {
                        var elem = document.createElement('tr') ; 
                        p = (( weights[i]*100 ) / capacite).toFixed(2) ; 
                        elem.innerHTML = "	<td > " + i + " </td> <td > " + affectation[i] + "  </td> <td>  " +weights[i]+"  </td>  <td class='pr-4'><div class='progress mr-4 mt-2' style='height: 20px;'><div class='progress-bar' role='progressbar' style='width: " +p + "%;' aria-valuenow='25' aria-valuemin='0' aria-valuemax='100'> "+p+" %</div></div></td>" ;
                        aff.append(elem) ;

                }
            }

         eel.expose(heurisjs);
        async function heurisjs(){
            var configs = [6];
            //--------------------------------------------------------
            var tab1 =[];
            tab1  = await eel.ffd_py(capacite,items)();
            var c1 = [];
            c1 = tab1[2];
            console.log(" configuration : "+c1)
            //loadtable(c1);
            //--------------------------------------------------------
            var tab2 =[];
            tab2  = await eel.ffi_py(capacite,items)();
            var c2 = [];
            c2 = tab2[2];
            console.log(" configuration : "+c2)
            //--------------------------------------------------------
            var tab3 =[];
            tab3  = await eel.bf_py(capacite,items)();
            var c3 = [];
            c3 = tab3[2];
            console.log(" configuration : "+c3)
            //--------------------------------------------------------
            var tab4 =[];
            tab4  = await eel.wf_py(capacite,items)();
            var c4 = [];
            c4 = tab4[2];
            console.log(" configuration : "+c4)
            //--------------------------------------------------------
            var tab5 =[];
            tab5 = await eel.awf_py(capacite,items)();
            var c5 = [];
            c5 = tab5[2];
            console.log(" configuration : "+c5)
            //--------------------------------------------------------
            var tab6 =[];
            tab6  = await eel.nf_py(capacite,items)();
            var c6 = [];
            c6 = tab6[2];
            console.log(" configuration : "+c6)
            configs[0]=tab1;configs[1]=tab2;configs[2]=tab3;configs[3]=tab4;configs[4]=tab5;configs[5]=tab6;
            //return configs;
            //console.log(" configuration : "+configs[6]+"&&[5]")



            
            function onRowClick(tableId,callback) {
                var table = document.getElementById(tableId),
                    rows = table.getElementsByTagName("tr"),
                    i;
                for (i = 0; i < rows.length; i++) {
                   
                    table.rows[i].onclick = function (row) {
                        return function () {

                            /* delete colors from others rows */ 

                            var trs = $(".hr_body tr") ; 
                            for(var i=0 ; i < trs.length ; i++ ){
                                trs[i].style.background = "white" ;
                            }

                            /*-------*/
                            
                            var k = configs[this.rowIndex-1];
                            
                            var Table = document.getElementById("tbody");
                            Table.innerHTML = "";
                            loadtable(k);
                            console.log("++++++++++ROW"+this.rowIndex);
                           
                            switch(this.rowIndex) {
                                case 1:
                                    $(this).css('background', '#B3D9DF');
                                  break;
                                case 2:
                                    $(this).css('background', '#FCFF9E');
                                  break;
                                  case 3:
                                    $(this).css('background', '#C7E9FF');
                                  break;
                                  case 4:
                                    $(this).css('background', '#D7F4C1');
                                  break;
                                  case 5:
                                    $(this).css('background', '#FFE197');
                                  break;
                                  case 6:
                                    $(this).css('background', '#DBDCC7');
                                  break;
                                default:
                                    $(this).css('background', 'transparent');
                              }
                            
                            callback(row);
                        };
                    }(table.rows[i]);
                }
            };
            onRowClick("my-table-id", function (row){
               
            });
        //------------------------------------------------------------------------
        }

        
  //______________________________________________________________________
        eel.expose(jsaffich1); // Expose this function to Python
        function jsaffich1(a,t) {
            document.getElementById("sol_bins1").innerHTML = a ; 
            document.getElementById("time1").innerHTML = t + " secondes" ;
        }
        eel.expose(jsaffich2);
        function jsaffich2(a,t) {
            document.getElementById("sol_bins2").innerHTML = a ; 
            document.getElementById("time2").innerHTML = t + " secondes" ;
        }
        eel.expose(jsaffich3);
        function jsaffich3(a,t) {
            document.getElementById("sol_bins3").innerHTML = a ; 
            document.getElementById("time3").innerHTML = t + " secondes" ;
        }
        eel.expose(jsaffich4);
        function jsaffich4(a,t) {
            document.getElementById("sol_bins4").innerHTML = a ; 
            document.getElementById("time4").innerHTML = t + " secondes" ;
        }
        eel.expose(jsaffich5);
        function jsaffich5(a,t) {
            document.getElementById("sol_bins5").innerHTML = a ; 
            document.getElementById("time5").innerHTML = t + " secondes" ;
        }
        eel.expose(jsaffich6);
        function jsaffich6(a,t) {
            document.getElementById("sol_bins6").innerHTML = a ; 
            document.getElementById("time6").innerHTML = t + " secondes" ;
        }
