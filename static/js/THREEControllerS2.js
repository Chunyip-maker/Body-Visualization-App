import * as THREE from 'three';
import { FBXLoader } from '/static/js/FBXLoader.js';
import { OrbitControls } from '/static/js//OrbitControls.js';
import Stats from '/static/js/stats.module.js';
import { Scene } from '/static/js//three.module.js';
import {MeshPhongMaterial} from '/static/js//MeshPhongMaterial.js';
import * as dat from 'https://cdn.jsdelivr.net/npm/dat.gui@0.7.9/build/dat.gui.module.js';

//init

let stats, mixer, canvas, canvasWidth, canvasHeight, clock;
let camera, scene, renderer, controls, group;
let loadModel, tempModel, action;


//test version for model under /static/model/test2/ folder only
init("canvas", "Breathing Idle2.fbx");



async function init(canvasID, modelName) {

    //canvas set up
    canvas = document.getElementById(canvasID);
    //document.body.appendChild(canvas);
    canvasWidth = document.getElementById(canvasID).clientWidth;
    canvasHeight = document.getElementById(canvasID).clientHeight;

    
    clock = new THREE.Clock();

    //set up camera
    camera = new THREE.PerspectiveCamera( 30, canvasWidth / canvasHeight, 0.1, 20);
    camera.position.set(1.66,2.05,3.61);
    //camera.rotation.set(-0.34, 0.51, 0.17);
    camera.lookAt(0,1,0);
    console.log(camera);


    //scene set up, background color debug use only
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xffffff);
    
    //set up render
    renderer = new THREE.WebGLRenderer( {antialias: true, alpha: true } );
    renderer.setSize( canvasWidth , canvasHeight );
    document.body.appendChild( renderer.domElement );
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.shadowMap.enabled = true;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1; 
    canvas.appendChild(renderer.domElement);



    //light
    const light = new THREE.AmbientLight(0xffffff,0.8);
    light.position.set(10.0, 10.0, 10.0).normalize();
    scene.add(light);
    var light2 = new THREE.DirectionalLight(0xffffff,1);
    light2.position.set(0, 3, 2);
    light2.castShadow = true;
    scene.add(light2);
    var light3 = new THREE.DirectionalLight(0xffffff,1);
    light3.position.set(0, 0, 2);
    light3.castShadow = true;
    scene.add(light3);


    //grid
    const gridHelper = new THREE.GridHelper(10, 10);
    gridHelper.receiveShadow = true;
    scene.add(gridHelper);


    //set up stats
    stats = new Stats();
    document.body.appendChild( stats.dom );

    //set up controller(enable user to control camera)
    controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true
    controls.target.set(0, 1, 0)
    controls.update()



    group = new THREE.Group();
    scene.add(group);

    //Async loader!
    const fbxLoader = new FBXLoader().setPath( '/static/model/test2/' );
    [loadModel, tempModel] = await Promise.all( [
        fbxLoader.loadAsync( 'Breathing Idle2.fbx' ),
        fbxLoader.loadAsync( 'Breathing Idle2.fbx' )
    ] );


    //animation
    group.add(loadModel);
    console.log(loadModel.children);
    mixer = new THREE.AnimationMixer( loadModel );
    action = mixer.clipAction( loadModel.animations[ 0 ] );
    action.play();
    //end animation
    loadModel.traverse( child => {

        if (child instanceof THREE.Mesh) {
            child.material.transparent = true;
            child.material.side = THREE.DoubleSide;
            child.material.alphaTest = 0.5;
            console.log(child.name);
    
        }
    })
    animate();
}


function animate() {
    requestAnimationFrame( animate );
    const delta = clock.getDelta();
    if ( mixer ) mixer.update( delta );
    renderer.render( scene, camera );
    stats.update();

}


function TextureChange(targetTextureName, newTexturePath) {
    loadModel.traverse( child => {
        if (child instanceof THREE.Mesh) {
            
            if (child.name == targetTextureName) {

                var newTexture = new THREE.TextureLoader().load(newTexturePath);
                child.material.map = newTexture;
                child.material.needsUpdate = true;

            }
        }
    })
}


//API of modify bones

let count = 0;
document.getElementById("testButton").onclick = function testButton(){
    //console.log("111");
    var input = document.getElementById("testButton").name;
    input = input.split(",");
    console.log(input[0], input[1]);
    if (count % 2 == 0) {
        TextureChange(input[0], input[1]);
        count += 1;
    } else {
        count = 0;
        TextureChange(input[1], input[0]);
    }
    
}


//clean texture, add gui, temp





//gui.hide();