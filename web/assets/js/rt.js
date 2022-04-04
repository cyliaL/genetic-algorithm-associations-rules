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
			$('.affectation')[0].innerHTML= '' ; 
		
			poids.innerHTML = Math.min (...items) + " < p < " + Math.max (...items) ; 
			c.innerHTML = capacite ; 
			nb.innerHTML = nombre_items ; 
			for(var i = 0 ; i <items.length ; i++) {
				var tr = document.createElement('tr') ; 
				tr.innerHTML=" <td> " +i + " </td> <td> " + items[i]+ "</td>" ; 
				objets.append (tr) ; 
			}
			
			document.getElementById("maxc").value =10 ; 
			document.getElementById("maxi").value =5000 ; 
			document.getElementById("maxn").value =1000 ; 

			document.getElementById("sol_bins").innerHTML = "" ; 
			document.getElementById("time").innerHTML ="" ; 
			 
		}
		async function loadtable(tableau){
        var obj = $(".body_objets2")[0] ;
        for(var i = 0 ; i <tableau.length ; i++) {
        var tr = document.createElement('tr') ; 
        tr.innerHTML=" <td> " +i + " </td> <td> " + tableau[i]+ "</td>" ; 
        obj.append (tr) ; 
    }
 }
          async function tsjs(){
			//eel.agpy(capacite,items);
			var tab =[];
            tab  = await eel.tspy(capacite,items)();
            var c = [];
            c = tab[2];
			d = tab[3];
            console.log(" configuration : "+c);
            //loadtable(c);
			jsaffich(tab[0],tab[1]);

			//-------------------
			var set =  new Set(tab[2])   ;
            var p = 0 ; 
			var list_bins  = Array.from(set);
			console.log("++++capacite+++"+capacite);
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
						weights[i] += d[j] ; 
					}
				}
				
			}
		console.log(weights) ; 
		$('.affectation')[0].innerHTML= '' ; 
		var aff = $('.affectation')[0] ; 
		for(i = 0 ; i<affectation.length ; i++ ) {
			var elem = document.createElement('tr') ; 
			p = (( weights[i]*100 ) / capacite ).toFixed(2); 
			elem.innerHTML = "	<td > " + i + " </td> <td > " + affectation[i] + "  </td> <td>  " +weights[i]+"  </td>  <td class='pr-4'><div class='progress mr-4 mt-2' style='height: 20px;'><div class='progress-bar' role='progressbar' style='width: " +p + "%;' aria-valuenow='25' aria-valuemin='0' aria-valuemax='100'> "+p+" %</div></div></td>" ;
			aff.append(elem) ;  

		}
		document.getElementById("sol_bins").innerHTML = tab[0] ; 
		document.getElementById("time").innerHTML = tab[1] + " secondes" ; 
		console.log("best = "+tab[2]);
		//loadtable(tab[2]);
			}
			
			eel.expose(jsaffich); // Expose this function to Python
			async function jsaffich(a,t) {
				document.getElementById("sol_bins").innerHTML = a ; 
				document.getElementById("time").innerHTML = t + " secondes" ;
			}
		
		
		