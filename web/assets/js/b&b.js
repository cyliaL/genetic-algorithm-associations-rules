var capacite = 0 ; 
var items = [] ; 
var nombre_items = 0 ; 
var solution = [] ; 

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
 
    document.getElementById("sol_bins").innerHTML = "" ; 
    document.getElementById("time").innerHTML ="" ; 
     

}


    

    //--------------------------------------------------------------------------

    

    async function loadtable(tableau){
        var obj = $(".body_objets2")[0] ;
        for(var i = 0 ; i <tableau.length ; i++) {
            var tr = document.createElement('tr') ; 
            tr.innerHTML=" <td> " +i + " </td> <td> " + tableau[i]+ "</td>" ; 
            obj.append (tr) ; 
        }
    }


    async function bnbjs(){

           

            var c = document.getElementById('capacite');
            capacite=  parseInt ( c.innerHTML ) ;  
            var tab =[];
            tab  = await eel.branchAndBound(items,capacite)();
            var c = tab[2];
            $('.affectation')[0].innerHTML  ='' ; 
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

    var aff = $('.affectation')[0] ; 
    for(i = 0 ; i<affectation.length ; i++ ) {
        var elem = document.createElement('tr') ; 
        p = (( weights[i]*100 ) / capacite ).toFixed(2) ; 
        elem.innerHTML = "	<td > " + i + " </td> <td > " + affectation[i] + "  </td> <td>  " +weights[i]+"  </td>  <td class='pr-4'><div class='progress mr-4 mt-2' style='height: 20px;'><div class='progress-bar' role='progressbar' style='width: " +p + "%;' aria-valuenow='25' aria-valuemin='0' aria-valuemax='100'> "+p+" %</div></div></td>" ;
        aff.append(elem) ;         
    }
}



eel.expose(jsaffich); // Expose this function to Python
function jsaffich(a,t) {
    document.getElementById("sol_bins").innerHTML = a ; 
    document.getElementById("time").innerHTML = t + " secondes" ;
}



// add items 
$('.add_items')[0].addEventListener('click', function(ev) {
    var item = parseInt ($('.input_items')[0].value) ;
    $('.input_items')[0].value = 0 ; 
    if( isNaN(item))  {
        alert('Objet Vide !') ; 
    }else {
        items.push(item) ;  
        var objets = $(".body_objets")[0] ;
        var tr = document.createElement('tr') ; 
        tr.innerHTML=" <td> " +( ( items.length )-1 )+ " </td> <td> " + item + "</td>" ; 
        objets.append (tr) ;  
        nombre_items ++ ; 
        $("#NB")[0].innerHTML  = nombre_items ; 
        var cell2 = document.getElementById('capacite');
        capacite=  parseInt ( cell2.innerHTML ) ; 
        $('#Poids')[0].innerHTML =  Math.min (...items) + " < p < " + Math.max (...items) ; 
    
        
    }
}) ; 

