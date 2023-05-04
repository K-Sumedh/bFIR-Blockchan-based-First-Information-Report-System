function toggle(target){
    
  // var artz = document.getElementsByClassName('article');
  var artz = document.getElementsByTagName('section');
  var targ = document.getElementById(target);  
  var isVis = targ.style.display=='block';
    
  // hide all
  for(var i=0;i<artz.length;i++){
    //  artz[i].style.display = 'none';
    // if (targ == artz[i] && targ.style.display == 'block')
    //   break;
    // else
     artz[i].style.display = 'none';
  }
  // toggle current
  targ.style.display = isVis?'none':'block';
    
  return false;
}
