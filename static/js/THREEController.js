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


    //GUI debug only, will remove later
    let gui = new dat.GUI();
    console.log("init run");
    const background_1 = {
    "color": 0xffffff
    };

    
    clock = new THREE.Clock();

    //set up camera
    camera = new THREE.PerspectiveCamera( 30, canvasWidth / canvasHeight, 0.1, 20);
    camera.position.set(1.66,2.05,3.61);
    //camera.rotation.set(-0.34, 0.51, 0.17);
    camera.lookAt(0,1,0);
    console.log(camera);


    //scene set up, background color debug use only
    scene = new THREE.Scene();
    scene.background = new THREE.Color(background_1.color);
    
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


    //fbx loader
    let boneMenu = [];
    let objectCopy = null;
    let modelObject;


    group = new THREE.Group();
    scene.add(group);


    //background color menu, debug only
    let displayFolder = gui.addFolder("Display");
    const material = new MeshPhongMaterial();
    displayFolder.addColor(background_1, "color").onChange((color) => {
        scene.background = new THREE.Color(background_1.color);
    });


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

    //debug use, should be called after the init finished.
    //all gui in this part will be remove later
    //current gui for debug only
    loadModel.traverse( child => {

        if (child.type == "Bone") {
                
                if ( !boneMenu.includes(child.name) && child.name.indexOf("J_Sec") == -1) {
                    let boneFolder = gui.addFolder(child.name);
                    boneFolder.add(child.scale, 'x', 0.9, 1.1).name("Scale" + " X");
                    boneFolder.add(child.scale, 'y',0.9, 1.1).name("Scale" + " Y");
                    boneFolder.add(child.scale, 'z',0.9, 1.1).name("Scale" + " Z");
                    boneFolder.add(child.position, 'x',0, 3).name("position" + " X");
                    boneFolder.add(child.position, 'y',0, 3).name("position" + " Y");
                    boneFolder.add(child.position, 'z',0, 3).name("position" + " Z");
                    console.log(child.name);
                    console.log(child);
                }

                boneMenu.push(child.name);
            }

        if (child instanceof THREE.Mesh) {


            child.material.transparent = true;
            child.material.side = THREE.DoubleSide;
            child.material.alphaTest = 0.5;
            console.log(child.name);
            

            if (child.name == "N00_001_01_Bottoms_01_CLOTH_(Instance)") {

                
                let temp = "/static/model/old_male/model1/Old Male.vrm.textures/_12.png"
                const bottom = ["1","2","3",temp];

                gui.add({ bottom: bottom[0]}, "bottom")
                .options(bottom)
                .onChange((val) => {
                    var newTexture = new THREE.TextureLoader().load(val);
                    child.material.map = newTexture;
                    child.material.needsUpdate = true;
                });

            }

            if (child.name == "N00_001_01_Bottoms_01_CLOTH_(Instance)") {

                
                let temp = "/static/model/old_male/model1/Old Male.vrm.textures/_12.png"
                const bottom = ["1","2","3",temp];

                gui.add({ bottom: bottom[0]}, "bottom")
                .options(bottom)
                .onChange((val) => {
                    var newTexture = new THREE.TextureLoader().load(val);
                    child.material.map = newTexture;
                    child.material.needsUpdate = true;
                });

            }

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

//API of modify bones

document.getElementById("a1").oninput = function changeHeight(){
    let index = calculateTransformation(1);

    loadModel.traverse( child => {
        if (child.type == "Bone") {

                if ( child.name == "") {

                }

        }
    })
}

document.getElementById("a2").oninput = function changeWeight(){
    let index = calculateTransformation(2);

    loadModel.traverse( child => {
        if (child.type == "Bone") {

                if ( child.name == "") {

                }

        }
    })
}


document.getElementById("a3").oninput = function changeChest(){
    let index = calculateTransformation(3);

    loadModel.traverse( child => {
        if (child.type == "Bone") {

                if ( child.name == "") {

                }

        }
    })
}

document.getElementById("a4").oninput = function changeWaist(){
    let index = calculateTransformation(4);

    loadModel.traverse( child => {
        if (child.type == "Bone") {

                if ( child.name == "") {

                }

        }
    })
}

document.getElementById("a5").oninput = function changeHip(){
    let index = calculateTransformation(5);

    loadModel.traverse( child => {
        if (child.type == "Bone") {

                if ( child.name == "") {

                }

        }
    })
}

document.getElementById("a6").oninput = function changeArm(){
    let index = calculateTransformation(6);

    loadModel.traverse( child => {
        if (child.type == "Bone") {

                if ( child.name == "") {

                }

        }
    })
}

document.getElementById("a7").oninput = function changeThigh(){
    let index = calculateTransformation(7);

    let countLeftLeg = 0;
    let countLeftKnee = 0;

    loadModel.traverse( child => {
        if (child.type == "Bone") {

                if ( child.name == "Left_leg" && countLeftLeg == 0) {
                    // console.log("------------");
                    // console.log("leg before:");
                    // console.log(child.scale.x);
                    child.scale.x += index;
                    child.scale.z += index;
                    // console.log("leg after:");
                    // console.log(child.scale.x);
                    // console.log("------------");
                    countLeftLeg++;
                }
                if ( child.name == "Right_leg") {
                    child.scale.x += index;
                    child.scale.z += index;
                }
                if ( child.name == "Left_knee" && countLeftKnee == 0) {
                    // console.log("=========");
                    // console.log("knee before:");
                    // console.log(child.scale.x);
                    // child.scale.x -= index;
                    // child.scale.z -= index;
                    // console.log("knee after:");
                    // console.log(child.scale.x);
                    // console.log(child);
                    // console.log("=========");
                    countLeftKnee++;
                }
                if ( child.name == "Right_knee") {
                    // child.scale.x -= index;
                    // child.scale.z -= index;
                }
        }
    })
}

document.getElementById("a8").oninput = function changeShank(){
    let index = calculateTransformation(8);

    loadModel.traverse( child => {
        if (child.type == "Bone") {

                if ( child.name == "Left_knee") {
                    child.scale.x += index;
                    child.scale.z += index;
                }
                if ( child.name == "Right_knee") {
                    child.scale.x += index;
                    child.scale.z += index;
                }
        }
    })
}


/* Get the information from the document and return index of actual scale*/
function calculateTransformation(id){
    let value = document.getElementById("a" + id).value;
    document.getElementById("b"  + id).innerText = value;
    let min = document.getElementById("a"  + id).min;
    let max = document.getElementById("a"  + id).max;
    let variance = value - getHistoryValue(id);
    let index = getScaleIndex(min, max, variance);
    setHistoryValue(id, value);
    return index;
}


let history_value_1 = document.getElementById("a1").value;
let history_value_2 = document.getElementById("a2").value;
let history_value_3 = document.getElementById("a3").value;
let history_value_4 = document.getElementById("a4").value;
let history_value_5 = document.getElementById("a5").value;
let history_value_6 = document.getElementById("a6").value;
let history_value_7 = document.getElementById("a7").value;
let history_value_8 = document.getElementById("a8").value;

/* Get the history value input*/
function getHistoryValue(id){
    switch (id){
        case 1:
            return history_value_1;
        case 2:
            return history_value_2;
        case 3:
            return history_value_3;
        case 4:
            return history_value_4;
        case 5:
            return history_value_5;
        case 6:
            return history_value_6;
        case 7:
            return history_value_7;
        case 8:
            return history_value_8;
    }
}

/* Set the history value input*/
function setHistoryValue(id, value){
    switch (id){
        case 1:
            history_value_1 = value;
            break;
        case 2:
            history_value_2 = value;
            break;
        case 3:
            history_value_3 = value;
            break;
        case 4:
            history_value_4 = value;
            break;
        case 5:
            history_value_5 = value;
            break;
        case 6:
            history_value_6 = value;
            break;
        case 7:
            history_value_7 = value;
            break;
        case 8:
            history_value_8 = value;
            break;
    }
}

/* Calculate the actual scale index to transform the model*/
function getScaleIndex(min, max, value){
    //range = 0.9 - 1.1, index = scale number
    let percentage = value / (max - min);
    let actualIndex = percentage * (0.2);
    return actualIndex;
}