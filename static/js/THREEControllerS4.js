import * as THREE from 'three';
import { FBXLoader } from '/static/js/FBXLoader.js';
import { GLTFLoader } from '/static/js/GLTFLoader.js';
import { OrbitControls } from '/static/js//OrbitControls.js';
import Stats from '/static/js/stats.module.js';
import { Scene } from '/static/js//three.module.js';
import * as dat from 'https://cdn.jsdelivr.net/npm/dat.gui@0.7.9/build/dat.gui.module.js';

//init

let stats, mixer, canvas, canvasWidth, canvasHeight, clock;
let camera, scene, renderer, controls;
let loadModel,action;

let stats1, mixer1, canvas1, clock1;
let camera1, scene1, renderer1, controls1;
let loadModel1,action1;


//test version for model under /static/model/test2/ folder only
init("before_canvas", "Breathing Idle2.fbx");
init1("after_canvas", "Breathing Idle2.fbx");

function sceneInit(canvasID) {
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
        //console.log(camera);

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

        controls.addEventListener( 'change', () => {
            camera1.position.copy( camera.position );
            camera1.rotation.copy( camera.rotation );
        } );
        //x=0.74,y=1.338,z=1.278 shang
        //x=0.7458 y = 0.69353, z=1.379
        
}   

async function init(canvasID, modelName) {

    // group = new THREE.Group();
    sceneInit(canvasID);

    //Async loader!
    const fbxLoader = new FBXLoader().setPath( '/static/model/test2/' );
    [loadModel] = await Promise.all( [
        fbxLoader.loadAsync( 'Breathing Idle2.fbx' )
    ] );


    loadModel.traverse( child => {

        if (child instanceof THREE.Mesh) {
            child.material.transparent = true;
            child.material.side = THREE.DoubleSide;
            child.material.alphaTest = 0.5;
        }
    })

    scene.add(loadModel);
    setFbxAnimation(loadModel);
    
}

function setFbxAnimation(model) {
    //animation
    mixer = new THREE.AnimationMixer( model );
    action = mixer.clipAction( model.animations[ 0 ] );
    action.play();
    animate();
    
}


function animate() {
    requestAnimationFrame( animate );
    const delta = clock.getDelta();
    if ( mixer ) mixer.update( delta );
    renderer.render( scene, camera );
    stats.update();
    //console.log(controls.target);
    // console.log(camera.position)
    // console.log(camera.rotation)
    
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


function sceneInit1(canvasID) {
    //canvas set up
    canvas1 = document.getElementById(canvasID);
    //document.body.appendChild(canvas);
    canvasWidth = document.getElementById(canvasID).clientWidth;
    canvasHeight = document.getElementById(canvasID).clientHeight;

    clock1 = new THREE.Clock();

    //set up camera
    camera1 = new THREE.PerspectiveCamera( 30, canvasWidth / canvasHeight, 0.1, 20);
    camera1.position.set(1.66,2.05,3.61);
    //camera.rotation.set(-0.34, 0.51, 0.17);
    camera1.lookAt(0,1,0);
    //console.log(camera);

    //scene set up, background color debug use only
    scene1 = new THREE.Scene();
    scene1.background = new THREE.Color(0xffffff);
    
    //set up render
    renderer1 = new THREE.WebGLRenderer( {antialias: true, alpha: true } );
    renderer1.setSize( canvasWidth , canvasHeight );
    document.body.appendChild( renderer1.domElement );
    renderer1.setPixelRatio( window.devicePixelRatio );
    renderer1.shadowMap.enabled = true;
    renderer1.toneMapping = THREE.ACESFilmicToneMapping;
    renderer1.toneMappingExposure = 1; 
    canvas1.appendChild(renderer1.domElement);

    //light
    const light = new THREE.AmbientLight(0xffffff,0.8);
    light.position.set(10.0, 10.0, 10.0).normalize();
    scene1.add(light);
    var light2 = new THREE.DirectionalLight(0xffffff,1);
    light2.position.set(0, 3, 2);
    light2.castShadow = true;
    scene1.add(light2);
    var light3 = new THREE.DirectionalLight(0xffffff,1);
    light3.position.set(0, 0, 2);
    light3.castShadow = true;
    scene1.add(light3);


    //grid
    const gridHelper = new THREE.GridHelper(10, 10);
    gridHelper.receiveShadow = true;
    scene1.add(gridHelper);

    //set up stats
    stats1 = new Stats();
    document.body.appendChild( stats1.dom );

    //set up controller(enable user to control camera)
    controls1 = new OrbitControls(camera1, renderer1.domElement)
    controls1.enableDamping = true
    controls1.target.set(0, 1, 0)
    controls1.update()
    

    controls1.addEventListener( 'change', () => {
        camera.position.copy( camera1.position );
        camera.rotation.copy( camera1.rotation );
    } );
}

async function init1(canvasID, modelName) {

    // group = new THREE.Group();
    sceneInit1(canvasID);

    //Async loader!
    const fbxLoader = new FBXLoader().setPath( '/static/model/test2/' );
    [loadModel1] = await Promise.all( [
        fbxLoader.loadAsync( 'Breathing Idle2.fbx' )
    ] );


    loadModel1.traverse( child => {

        if (child instanceof THREE.Mesh) {
            child.material.transparent = true;
            child.material.side = THREE.DoubleSide;
            child.material.alphaTest = 0.5;
        }
    })

    scene1.add(loadModel1);
    setFbxAnimation1(loadModel1);

}

function setFbxAnimation1(model) {
//animation
    mixer1 = new THREE.AnimationMixer( model );
    action1 = mixer1.clipAction( model.animations[ 0 ] );
    action1.play();
    animate1();
}


function animate1() {
    requestAnimationFrame( animate1 );
    const delta = clock1.getDelta();
    if ( mixer1 ) mixer1.update( delta );
    renderer1.render( scene1, camera1 );
    stats1.update();
}

document.getElementById("Top").onclick = function cameraChange() {


    camera.position.set(0.6248297296327294, 1.503963156706119, 1.3563233589083084);
    camera1.position.set(0.6916297296327294, 1.503963156706119, 1.3563233589083084);

    camera.rotation.set(-0.2830493492651662, 0.4157931856541107, 0.11694632498187489);
    camera1.rotation.set(-0.2830493492651662, 0.4157931856541107, 0.11694632498187489);
    controls.target.set(
        -0.025193594935890188,
        1.133358866462773,
        0.012610338156221673);
    controls.update();


}

document.getElementById("Bottom").onclick = function cameraChange() {
    camera.position.set(0.5902717381883454, 0.9486176075421906, 1.5785914227370572);
    camera1.position.set(0.5902717381883454, 0.9486176075421906, 1.5785914227370572);

    camera.rotation.set(-0.2830493492651662, 0.4157931856541107, 0.11694632498187489);
    camera1.rotation.set(-0.2830493492651662, 0.4157931856541107, 0.11694632498187489);

    controls.target.set(
        -0.046407628814892146,
        0.4610626823169693,
        -0.0650557742511241);
    controls.update();
}





