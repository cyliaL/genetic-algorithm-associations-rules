// get files and items , execute algorithms 

document.querySelector("#file-upload-1").onchange = async function(){
    document.querySelector("#file-name").textContent ="loaded" ; 
    document.querySelector("#bar-chart-1").innerHTML = '' ; 
    var text = "" ; 
    var names = [] ; 
    var list = [ ] ; 
    var capacite = [] ;  
    var nombre_items =  [] ; 
    var items = [] ; 
    for ( var i = 0 ; i < this.files.length ; i++ ){
        text = await (new Response(this.files[i]).text());
        names[i] = this.files[i].name ; 
        list= text.split('\n') ;
        list = list.map(function (x) { return parseInt(x); });
        capacite[i] =  list[1]  ; 
        nombre_items[i] = list[0] ; 
        items[i] = list.slice(2 , list[0]+2 ) ;

    }
    var solutions= [];
    var FFD = []
    var FFI = [] ; 
    var BF = [] ; 
    var wf = [] ; 
    var awf = [] ; 
    var nf = [] ;  
    var tab = [] ;  

    for( i=0 ; i < items.length ; i++ ) {
        // execute les heuristiques et recuperer les resultats dans deux tableaux temps[][] et solutions[][] , pour chaque instances le reusltat de chaque heuristique ;   
        //-------------------FFD----------------- 

            tab  = await ( eel.ffd_py(capacite[i],items[i])());
            FFD[i] = tab[0];
            
    //---------------------------------------
    //-------------------FFI-----------------
            
            tab  = await eel.ffi_py(capacite[i],items[i])();
            FFI[i] = tab[0];
    //---------------------------------------
    //-------------------BF-----------------
            tab =[];
            tab  = await eel.bf_py(capacite[i],items[i])();
            BF[i] = tab[0];
    //---------------------------------------
    //-------------------WF-----------------
            tab =[];
            tab  = await eel.wf_py(capacite[i],items[i])();
            wf[i] = tab[0];
    //---------------------------------------
    //-------------------AWF-----------------
            tab =[];
            tab  = await eel.awf_py(capacite[i],items[i])();
            awf[i] = tab[0];
    //---------------------------------------
    //-------------------NF-----------------
            tab =[];
            tab  = await eel.nf_py(capacite[i],items[i])();
            nf[i] = tab[0];
    //---------------------------------------
    }

    Bars(FFD , FFI , BF , wf  , nf , names) ; 

       
}



/*----------------------------------------------------------------------------------------------*/

document.querySelector("#file-upload-2").onchange = async function(){
    document.querySelector("#file-name2").textContent ="loaded" ; 
    document.querySelector("#line-chart-2").innerHTML = '' ; 
    var text = "" ; 
    var names = [] ; 
    var list = [] ; 
    var capacite = [] ;  
    var nombre_items =  [] ; 
    var items = [] ; 
    for ( var i = 0 ; i < this.files.length ; i++ ){
        text = await (new Response(this.files[i]).text());
        names[i] = this.files[i].name ; 
        list= text.split('\n') ;
        list = list.map(function (x) { return parseInt(x); });
        capacite[i] =  list[1]  ; 
        nombre_items[i] = list[0] ; 
        items[i] = list.slice(2 , list[0]+2 ) ;

    }
   
    var BF = [] ; 
    var tab = [] ;  
    var RS = [] ; 
    var RT = [] ; 
    var AG = [] ; 
    var timeBF = [] ,  timeRS = [] , timeAG = [] , timeRT = [] ; 

    for( i=0 ; i < items.length ; i++ ) {
       
        //---------------------BF----------------------
        tab =[];
        tab  = await ( eel.bf_py(capacite[i],items[i])() ) ;
        BF[i] = tab[0];
        timeBF[i] = tab[1] ; 

        //-------------------RS----------------------
        tab =[];
        tab  =  recuit_simule(items[i] , capacite[i]  , 0.95 , 1000 , 0.1 , 50  ) ;
        RS[i]  = tab[0] ; 
        timeRS[i] = tab[1] ; 

        //RT
        tab =[];
        tab  = await eel.tspy(capacite[i],items[i])();
        RT[i] = tab[0] ; 
        timeRT[i] = tab[1] ; 

        //AG
        tab =[];
        tab  = await eel.agpy(items[i],capacite[i])();
        AG[i] = tab[0] ; 
        timeAG[i] = tab[1] ; 

    
    }

    line2(RS , BF , RT , AG ,names ) ; 
    line1(timeRS , timeBF , timeRT , timeAG , names) ; 
      
}




/*************************************************************************************************** */



/*function for line chart 2 */  
function line2(RS , BF , RT , AG , names) {
    var options = {
        chart: {
            height: 350,
            type: 'line',
            zoom: {
                enabled: false
            },
        },
        dataLabels: {
            enabled: false
        },
        stroke: {
            width: 5 , 
            curve: 'straight',
            dashArray: [0, 0, 0]
        },
        colors: ["#0e9e4a", "#ffba57", "#ff5252" ,"#4680ff"],
        series: [{
                name: "RS",
                data: RS
            },
            {
                name: "AG",
                data: AG ,
            },
            {
                name: 'RT',
                data: RT , 
            },
            {
                name: 'BF',
                data: BF , 
            }
        ],
        title: {
            text: 'Solutions ( nombre des bins )',
            align: 'left'
        },
        markers: {
            size: 0,

            hover: {
                sizeOffset: 6
            }
        },
        xaxis: {
            categories: names ,
            title : {
                text : 'Instances'
            }
        },
         markers: {
          size: 4,
          colors: ["#FFA41B"],
          strokeColors: "#fff",
          strokeWidth: 2,
          hover: {
            size: 7,
          }
        },
        tooltip: {
            y: {
                title: {
                    formatter: function(val) {
                        return val + " (bins)"
                    }
                }
            }
        },
        grid: {
            borderColor: '#f1f1f1',
        }
    }
    document.querySelector("#line-chart-2").innerHTML = '' ; 
    var chart = new ApexCharts(
        document.querySelector("#line-chart-2"),
        options
    );
    chart.render();
};




function Bars(FFD , FFI , BF , wf   , nf , names) {
    var options = {
        chart: {
            height: 350,
            type: 'bar',
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '55%',
                endingShape : 'rounded' , 
               
            },
        },
        dataLabels: {
            enabled: true 
        },
        colors: ["#0e9e4a", "#4680ff", "#ff5252" , "#ffba57" , "#00acc1" , "#9ccc65" , "#20c997"],
        stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
        },
        series: [{
            name: 'FFD',
            data: FFD , 
        }, {
            name: 'FFI',
            data: FFI , 
        }, {
            name: 'BF',
            data: BF , 
        },
        {
            name: 'WF',
            data: wf , 
        },
      
        {
            name: 'NF',
            data: nf , 
        }],
        xaxis: {
            categories: names,
            title: {
                text: 'Instances'
            }
        },
        
        yaxis: {
            title: {
                text: 'Solutions'
            }
        },
       
        fill: {
            opacity: 1

        },
        tooltip: {
            y: {
                formatter: function(val) {
                    return val + " Bins"
                }
            }
        }
    }
    document.querySelector("#bar-chart-1").innerHTML = '' ; 
    var chart = new ApexCharts(
        document.querySelector("#bar-chart-1"),
        options
    );
    chart.render();
};




/*function for line chart 1 */ 
function line1(RS , BF , RT , AG , names) {
    var options = {
        chart: {
            height: 350,
            type: 'line',
            zoom: {
                enabled: false
            },
        },
        dataLabels: {
            enabled: false
        },
        stroke: {
            width: 5 , 
            curve: 'straight',
            dashArray: [0, 0, 0]
        },
        colors: ["#0e9e4a", "#ffba57", "#ff5252" ,"#4680ff"],
        series: [{
                name: "Temps RS",
                data: RS
            },
            {
                name: "Temps AG",
                data: AG ,
            },
            {
                name: 'Temps RT',
                data: RT , 
            },
            {
                name: 'Temps BF',
                data: BF , 
            }
        ],
        title: {
            text: 'Temps éxécution( ms )',
            align: 'left'
        },
        markers: {
            size: 4,
            colors: [ "#ff5252"],
            strokeColors: "#fff",
            strokeWidth: 2,
            hover: {
              size: 7,
            }
          },
        xaxis: {
            categories: names ,
            title : {
                text : 'Instances'
            }
        },
        tooltip: {
            y: {
                title: {
                    formatter: function(val) {
                        return val + " (bins)"
                    }
                }
            }
        },
        grid: {
            borderColor: '#f1f1f1',
        }
    }
    document.querySelector("#line-chart-1").innerHTML = '' ; 
    var chart = new ApexCharts(
        document.querySelector("#line-chart-1"),
        options
    );
    chart.render();
};




async function loadFile(file) {
    let text = await (new Response(file)).text();
    var list= text.split('\n') ;
    var list = list.map(function (x) { return parseInt(x); });
    capacite =  list[1]  ; 
    nombre_items = list[0] ; 
    items = list.slice(2 , list[0]+2 ) ;



}