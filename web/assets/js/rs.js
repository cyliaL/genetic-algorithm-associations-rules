// variables globales

var capacite = 0 ; 
var items = [] ; 
var nombre_items = 0 ; 
var solution = [] ; 



// add instance 

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
    var aff = $('.affectation')[0] ; 
    aff.innerHTML='' ; 
    poids.innerHTML = Math.min (...items) + " < p < " + Math.max (...items) ; 
    c.innerHTML = capacite ; 
    nb.innerHTML = nombre_items ; 
    for(var i = 0 ; i <items.length ; i++) {
        var tr = document.createElement('tr') ; 
        tr.innerHTML=" <td> " +i + " </td> <td> " + items[i]+ "</td>" ; 
        objets.append (tr) ; 
    }
    document.getElementById("Tmax").value =1000 ; 
    document.getElementById("Tmin").value =0.1 ; 
    document.getElementById("iter").value =50 ; 
    document.getElementById("alpha").value =0.95 ; 
    document.getElementById("sol_bins").innerHTML = "" ; 
    document.getElementById("time").innerHTML ="" ; 

}



// FFD function 

function FFD (w , c ) {
    var order = Array.from(Array(w.length).keys()).sort((a, b) => w[a] > w[b] ? -1 : (w[b] > w[a]) | 0) ; 
    var bin_for_item = new Array(w.length) ; 
    bin_for_item.fill(-1) ;
    var bin_space = [] ; 
    var i = 0 ; 
    for ( var k=0 ; k< order.length ; k++) {
        i = order[k] ; 
        for(var j = 0 ; j < bin_space.length; j++) {
            if ( w[i]<bin_space[j] ){
                bin_for_item[i]=j ; 
                bin_space[j] -= w[i] ; 
                break ; 
            }
        }
        if ( bin_for_item[i] < 0 ) {
            j = bin_space.length ; 
            bin_for_item[i] = j ; 
            bin_space.push(c-w[i]) ;  
        } 
    }
    n_bin = bin_space.length ; 
    return bin_for_item  ; 
}


 /*--------------------------------------------objective function----------------------------------------------------*/

function   eval_fct ( config) {
    var nb_bins = Math.max(...config)+1 ; 
    var weights = new Array(nb_bins) ; weights.fill(0) ;
    var eval  = 0 ; 
    var i = 0 , j=0  ; 
    for (  i =0 ; i < config.length ; i++ ) {
        weights[config[i]] += items[i] ; 
    }
    for(j= 0 ; j < weights.length ; j++) {
        eval += Math.pow(  weights[j]  , 2 )  ; 
    }
    return eval; 
}




/*----------------------------------------------- get random solution-----------------------------------------------*/

function getsoluce( config  , T_moy , T) {
    var voisin  ; 
    if ( T <  T_moy ) {
        voisin  = mouv_basseT (config ); 
    }
    else {
        voisin  = mouv_hauteT (config ); 
    }
    return voisin ; 
}


/*---------------------------------------verify solution -----------------------------------------------------------*/

function verified_solution(config) {
    var nb_bins =  Math.max(...config)+1 ; 
    var weights = new Array(nb_bins) ; weights.fill(0) ;
    var verified = true , k= 0 ; 
    while(  k < config.length ) {
        weights[config[k]] += items[k] ;
        if (weights[config[k]]> capacite) {verified = false ; break } ; 
        k++  ; 
    }
    return verified ; 
}

/*----------------------------------------------high temperature move ----------------------------------------------*/

function mouv_hauteT (config) {
    var result = config.slice(0) ; 
    while ( true) {
        result = config.slice(0) ;
        var i = Math.floor(Math.random() * config.length) ; 
        var j = Math.floor(Math.random() * config.length) ; 
        [result[i], result[j]]= [result[j], result[i]] ;
        if(result == config) continue ; 
        if (verified_solution(result) ) break ; 
        }
    return result ; 
}

/*----------------------------------------------low temperature move -----------------------------------------------*/

function mouv_basseT (config) {
    var result = config.slice(0) ; 
    var set =  new Set(config)   ; 
    var list_bins  = Array.from(set);
    while ( true ) {
        result = config.slice(0) ;
        var i = Math.floor(Math.random() * config.length) ; 
        var j = Math.floor(Math.random() * (  set.size ) ) ; 
        result[i] = list_bins[j] ;  
        if(result == config) continue ; 
        if (verified_solution(result) ) break ; 
        }
    return result ; 
}



/*--------------------------------------------------main algorithme-------------------------------------------------*/

function recuit_simule(item , c  , alpha , T_initial , T_cible , nb_it) { 
    items = item ; 
    capacite = c ;  
    var sol = FFD( items , capacite).slice(0)  ;  
    solution = sol ; 
    var startTime = new Date().getTime();
    var x = sol.slice(0) ; 
    var T = T_initial ;
    var fx = eval_fct(sol ) ;
    var i=0 , y= 0 , fy = 0 , delta =0 , u =0  ;
    var expo = 0 ;
    var T_moy =  ( T_cible + T_initial ) / 2 ;
    var best = sol.slice(0) ; 
    while ( T > T_cible) {
        for(i = 0 ; i<= nb_it ;  i++ ) {
            y = getsoluce ( x , T_moy , T) ; 
            if( y == x ) continue ; 
            fy = eval_fct(y) ;
            delta = fy - fx ; 
            if (  delta > 0 ) {
                x = y.slice(0) ; 
                fx = fy ;  
            }
            else {
                u = Math.random() ;
                expo  = Math.exp( ( delta)/T) ;  
                if(u < expo ) {
                        x= y.slice(0) ; 
                        fx = fy ;  
                }
            }
            if(   (eval_fct(best)< eval_fct(x) )    || ( new Set(best)  ).size > ( new Set(x)  ).size )  { best = x.slice(0) }; 
        }
        T = T *alpha ; 
    }
    var nb_bins_RS = ( new Set(best)  ).size; 
    var elapsedTime =  ( new Date().getTime() - startTime ) / 1000  ;
    return  [ nb_bins_RS , elapsedTime , best ] ; 
    }





/* clic button run rs----------------------------------------------------------------------------------------------- */


 function run_recuit_simule() {
    var Tmax = parseInt( document.getElementById("Tmax").value ); 
    var Tmin = parseFloat( document.getElementById("Tmin").value )  ;  
    var iter =parseInt( document.getElementById("iter").value ); 
    var alpha = parseFloat( document.getElementById("alpha").value)  ; 
    var RS_sol = recuit_simule(items , capacite  , alpha , Tmax , Tmin , iter ) ;
    var set =  new Set(RS_sol[2])   ;
    var p = 0 ; 
    var aff = $('.affectation')[0] ; 
    aff.innerHTML='' ; 
    var list_bins  = Array.from(set);
    var weights = new Array(list_bins.length); 
    weights.fill(0) ;
    var affectation = new Array( RS_sol[0]) ; 
    for(var k = 0 ; k< RS_sol[0] ; k++ ) {
        affectation[k] = [] ;  

    }
    for ( var i= 0 ; i < affectation.length ; i++ ) {
        for(var j = 0 ; j< RS_sol[2].length; j++) {
            if(RS_sol[2][j]==list_bins[i]) {
                affectation[i].push(j) ; 
                weights[i] += items[j] ; 
            }
        }
        
    }
    for(i = 0 ; i<affectation.length ; i++ ) {
        var elem = document.createElement('tr') ; 
        p = (( weights[i]*100 ) / capacite ).toFixed(2) ; 
        elem.innerHTML = "	<td > " + i + " </td> <td > " + affectation[i] + "  </td> <td>  " +weights[i]+"  </td>  <td class='pr-4'><div class='progress mr-4 mt-2' style='height: 20px;'><div class='progress-bar' role='progressbar' style='width: " +p + "%;' aria-valuenow='25' aria-valuemin='0' aria-valuemax='100'> "+p+" %</div></div></td>" ;
        aff.append(elem) ;  

    }
    document.getElementById("sol_bins").innerHTML = RS_sol[0] ; 
    document.getElementById("time").innerHTML = RS_sol[1] + " secondes" ; 
}





 /*--------------------------------------------chart rs rt bf ag------------------------------------------------------*/


 