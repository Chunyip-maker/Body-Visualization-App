import * as THREE from 'three';
import { FBXLoader } from '/static/js/FBXLoader.js';
import { OrbitControls } from '/static/js//OrbitControls.js';
import Stats from '/static/js/stats.module.js';
import { Scene } from '/static/js//three.module.js';
import {MeshPhongMaterial} from '/static/js//MeshPhongMaterial.js';

import * as dat from 'https://cdn.jsdelivr.net/npm/dat.gui@0.7.9/build/dat.gui.module.js';
import {BoxGeometry, DoubleSide, Mesh, MeshBasicMaterial, TextureLoader} from "three";
import { Vector3 } from 'three';
//init

let stats, mixer, canvas, canvasWidth, canvasHeight, clock;
let camera, scene, renderer, controls, group;
let loadModel, tempModel, action;
let modelBoneName = [], bonePositionY = [];


//test version for model under /static/model/test2/ folder only
init("canvas");


//for new stage
var initPosition = 0.23;
var currentPosition;
//end of new variable

async function init(canvasID) {

    //canvas set up
    canvas = document.getElementById(canvasID);
    //document.body.appendChild(canvas);
    canvasWidth = document.getElementById(canvasID).clientWidth;
    canvasHeight = document.getElementById(canvasID).clientHeight;


    //GUI debug only, will remove later
    //let gui = new dat.GUI();
    console.log("init run");
    const background_1 = {
    "color": 0xffffff
    };

    
    clock = new THREE.Clock();

    //set up camera
    camera = new THREE.PerspectiveCamera( 30, canvasWidth / canvasHeight, 0.1, 100);
    //camera.position.set(1.66,2.05,3.61);
    camera.position.set(1.4485807979862497,2.0668476949423362,3.934246459224377);
    //camera.rotation.set(-0.34, 0.51, 0.17);
    camera.lookAt(0,1,0);
    //console.log(camera);


    //scene set up, background color debug use only
    scene = new THREE.Scene();
    //scene.background = new THREE.Color(background_1.color);
    scene.background = new THREE.Color(0xD6E7C5);
    //set up render
    renderer = new THREE.WebGLRenderer( {antialias: true, alpha: true } );
    renderer.setSize( canvasWidth , canvasHeight );
    document.body.appendChild( renderer.domElement );
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.shadowMap.enabled = true;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1;
    //renderer.outputEncoding = THREE.sRGBEncoding;
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
    // const gridHelper = new THREE.GridHelper(10, 10);
    // gridHelper.receiveShadow = true;
    // scene.add(gridHelper);

    // //Skybox ((( COMPLETE BUT NOT IN FINAL PRODUCT )))
    // let textureLoader = new TextureLoader();
    // let skyBoxGeometry = new BoxGeometry(40, 40, 40);
    // //the textures pattern in skybox material is left, right, up, down, front, back, px, nx, py, ny, pz, nz
    // //current scene: 13, 14_b, 20, 21, 23_b
    // let skyBoxMaterial = [
    //     new MeshBasicMaterial({ map: textureLoader.load('./static/background/png/20/px.png'), side: DoubleSide}),
    //     new MeshBasicMaterial({ map: textureLoader.load('./static/background/png/20/nx.png'), side: DoubleSide}),
    //     new MeshBasicMaterial({ map: textureLoader.load('./static/background/png/20/py.png'), side: DoubleSide}),
    //     new MeshBasicMaterial({ map: textureLoader.load('./static/background/png/20/ny.png'), side: DoubleSide}),
    //     new MeshBasicMaterial({ map: textureLoader.load('./static/background/png/20/pz.png'), side: DoubleSide}),
    //     new MeshBasicMaterial({ map: textureLoader.load('./static/background/png/20/nz.png'), side: DoubleSide})
    // ];
    // let skyboxMesh = new Mesh(skyBoxGeometry, skyBoxMaterial);
    // skyboxMesh.position.set(0, -3, 0);
    // scene.add(skyboxMesh);


    //set up stats
    // stats = new Stats();
    // document.body.appendChild( stats.dom );

    //set up controller(enable user to control camera)
    controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true
    controls.target.set(0, 1, 0)
    controls.update()

    controls.minPolarAngle = 0;
    controls.maxPolarAngle =  Math.PI * 0.5;
    //fbx loader
    let boneMenu = [];
    let objectCopy = null;
    let modelObject;


    group = new THREE.Group();
    scene.add(group);


    //background color menu, debug only
    //let displayFolder = gui.addFolder("Display");
    // const material = new MeshPhongMaterial();
    // displayFolder.addColor(background_1, "color").onChange((color) => {
    //     scene.background = new THREE.Color(background_1.color);
    // });


    //Async loader!
    let path = document.getElementById("model_path").innerText;
    const fbxLoader = new FBXLoader().setPath(path);
    [loadModel, tempModel] = await Promise.all( [
        fbxLoader.loadAsync( 'Idle.fbx' ),
        fbxLoader.loadAsync( 'Idle.fbx' )
    ] );

    //Read database store texture
    var hair_color = document.getElementById("hair_color").innerText;
    var skin_color = document.getElementById("skin_color").innerText;
    var top_dress = document.getElementById("top_dress").innerText;
    var bottom_dress = document.getElementById("bottom_dress").innerText;
    readInput(hair_color);
    readInput(skin_color);
    readInput(top_dress);
    readInput(bottom_dress);


    //Save the origin bones position data.

    loadOriginBones(modelBoneName, bonePositionY);

    //Alter history data
    loadModel.position.set(0,initPosition,0);
    if(document.getElementById("check_new_model").innerText != 0){
        loadingHistoryBodyData();
    }

    //animation
    group.add(loadModel);
    //console.log(loadModel.children);
    mixer = new THREE.AnimationMixer( loadModel );
    action = mixer.clipAction( loadModel.animations[ 0 ] );
    action.play();
    //end animation

    //debug use, should be called after the init finished.
    //all gui in this part will be remove later
    //current gui for debug only
    loadModel.traverse( child => {

        if (child instanceof THREE.Mesh) {

            child.material.transparent = true;
            child.material.side = THREE.DoubleSide;
            child.material.alphaTest = 0.5;
        }
    })

    //new stage
    const stageLoader = new FBXLoader().setPath("/static/model/test/");
    var [stage] = await Promise.all([
        stageLoader.loadAsync("Podium.fbx")
    ]);
    var list = []
    for (var i = 0; i < stage.children.length;i++) {
        if (stage.children[i].name != "Camera"
        &&stage.children[i].name != "Light" &&
        stage.children[i].name != "Light002"
        ) {
            list.push(stage.children[i]);
        }

    }
    stage.children = list;
    group.add(stage);

    scene.traverse(child =>{
        if (child instanceof THREE.Mesh) {
            child.frustumCulled = false;
        }
    })
    stage.scale.multiplyScalar(0.004);
    
    // console.log(loadModel);
    // console.log(loadModel.position);

    //loadVrmModel.translateY(1.0);
    console.log(stage)
    //end stage
    animate();
}


function animate() {
    TWEEN.update();
    requestAnimationFrame( animate );
    const delta = clock.getDelta();
    if ( mixer ) mixer.update( delta );
    renderer.render( scene, camera );
    //console.log(camera.position, controls.target)
    //stats.update();
}

//Method for changing the body due to parameter
function loadingHistoryBodyData(){
    changeHeightImpl();
    changeWeightImpl();
    changeThighImpl();
    changeShankImpl();
    changeHipImpl();
    changeArmGrithImpl();
    changeArmsPanImpl();
    changeWaistImpl();
    changeChestImpl();
}



//API of modify bones

document.getElementById("a1").oninput = function changeHeight(){
    changeHeightImpl();
}

var prevIndex = 1;
var callOnce = [0,0,0];
function changeHeightImpl(){
    let index = calculateTransformation(1, 0.2);
    changeScaleX(["Hips"], [], index);
    changeScaleY(["Hips"], [], index);
    changeScaleZ(["Hips"], [], index);
    
    //new stage/environment
    positionTranslate(index);
    //console.log(index)
    if (index > 0.93 && index < 1.03 && callOnce[0] == 0) {
        callOnce = [0 ,0 ,0];
        callOnce[0] = 1;
        cameraPositionOrigin();
    }
    if (index >= 1.03 && callOnce[1] == 0) {
        callOnce = [0 ,0 ,0];
        callOnce[1] = 1;
        cameraPositionHigh();
    }
    if (index <= 0.93 && callOnce[2] == 0) {
        callOnce = [0 ,0 ,0];
        callOnce[2] = 1;
        cameraPositionLow();
    }
}

//new feature camera
function cameraPositionOrigin() {
    const cameraTarget = new Vector3(1.1297525756088347, 2.1543632778727355, 4.013221907024572)
    const controlTarget = new Vector3(0,
        1,
        0)
    animateCamera(camera.position, controls.target,cameraTarget,controlTarget)
}

//new feature camera
function cameraPositionLow() {
    const cameraTarget = new Vector3(1.1103991149486863, 2.1710353733201555, 3.3357958987540135)
    const controlTarget = new Vector3(0.017290990949987674,
        0.9664811149186596,
        -0.053962235011330704)
    animateCamera(camera.position, controls.target,cameraTarget,controlTarget)
}
//new feature camera
function cameraPositionHigh() {
    const cameraTarget = new Vector3(1.3914624363865524, 2.369216508506059, 4.652770183181438)
    const controlTarget = new Vector3(0,
        1,
        0)
    animateCamera(camera.position, controls.target,cameraTarget,controlTarget)
}

//new feature stage/environment
function positionTranslate(index) {
    loadModel.position.set(0,initPosition + (index-1),0);
}

document.getElementById("a2").oninput = function changeWeight(){
    changeWeightImpl();
}

function changeWeightImpl(){
    let index = calculateTransformation(2, 0.1);
    changeScaleX(["Hips"], [], index);
    changeScaleZ(["Hips"], [], index);
}

document.getElementById("a3").oninput = function changeChest(){
    changeChestImpl();
}

function changeChestImpl(){
    let index = calculateTransformation(3, 0.2);
    changeScaleZ(["Upper_Chest"], ["Neck"], index);
}

document.getElementById("a4").oninput = function changeWaist(){
    changeWaistImpl();
}

function changeWaistImpl(){
    let path = document.getElementById("model_path").innerText;
    let index;
    if(path.indexOf("female") != -1){
        index = calculateTransformation(4, 0.3);
    }else{
        index = calculateTransformation(4, 0.2);
    }
    changeScaleX(["Spine"], ["Chest"], index);
    changeScaleZ(["Spine"], ["Chest"], index);
}

document.getElementById("a5").oninput = function changeHip(){
    changeHipImpl();
}

function changeHipImpl(){
    let index = calculateTransformation(5, 0.2);
    changeScaleZ(["Hips"], ["Left_leg", "Right_leg", "Spine"], index);
}

document.getElementById("a6").oninput = function changeArmGrith(){
    changeArmGrithImpl();
}

function changeArmGrithImpl(){
    let index = calculateTransformation(6, 0.4);
    changeScaleX(["Left_arm", "Right_arm"], [], index);
    changeScaleZ(["Left_arm", "Right_arm"], [], index);
}

document.getElementById("a7").oninput = function changeArmsPan(){
    changeArmsPanImpl();
}

function changeArmsPanImpl(){
    let index = calculateTranslationY(7, 0.04, "Left_arm", modelBoneName, bonePositionY);
    changePositionY(["Left_arm", "Right_arm"], [], index);
}

document.getElementById("a8").oninput = function changeThigh(){
    changeThighImpl();
}

function changeThighImpl(){
    let index = calculateTransformation(8, 0.3);
    changeScaleX(["Left_leg", "Right_leg"], ["Left_knee", "Right_knee"], index);
    changeScaleZ(["Left_leg", "Right_leg"], ["Left_knee", "Right_knee"], index);
}

document.getElementById("a9").oninput = function changeShank(){
    changeShankImpl();
}

function changeShankImpl(){
    let index = calculateTransformation(9, 0.3);
    changeScaleX(["Left_knee", "Right_knee"], [], index);
    changeScaleZ(["Left_knee", "Right_knee"], [], index);
}

/* Scale up and scale down the bones in the list */
function changeScaleX(scaleUpBones, scaleDownBones, index){
    loadModel.traverse( child => {
        if (child.type == "Bone") {
                if ( scaleUpBones.includes(child.name)) {
                    child.scale.x = index;
                    let i = scaleUpBones.indexOf(child.name);
                    scaleUpBones.splice(i, 1);

                    for(let j = 0; j < child.children.length; j++){
                        if(child.children[j].name.indexOf("J_Sec") == - 1 && scaleDownBones.includes(child.children[j].name)){
                            let test = 2 - index;
                            child.children[j].scale.x = test;
                        }
                    }
                }
        }
    })
}

/* Scale up and scale down the bones in the list */
function changeScaleZ(scaleUpBones, scaleDownBones, index){
    loadModel.traverse( child => {
        if (child.type == "Bone") {
                if ( scaleUpBones.includes(child.name)) {
                    child.scale.z = index;
                    let i = scaleUpBones.indexOf(child.name);
                    scaleUpBones.splice(i, 1);
                    for(let j = 0; j < child.children.length; j++){
                       if(child.children[j].name.indexOf("J_Sec") == -1 && scaleDownBones.includes(child.children[j].name)){
                           let test = 2 - index;
                           child.children[j].scale.z = test;
                       }
                    }
                }

        }
    })
}

/* Scale up and scale down the bones in the list */
function changeScaleY(scaleUpBones, scaleDownBones, index){
    loadModel.traverse( child => {
        if (child.type == "Bone") {
                if ( scaleUpBones.includes(child.name)) {
                    child.scale.y = index;
                    let i = scaleUpBones.indexOf(child.name);
                    scaleUpBones.splice(i, 1);
                    for(let j = 0; j < child.children.length; j++){
                       if(child.children[j].name.indexOf("J_Sec") == -1 && scaleDownBones.includes(child.children[j].name)){
                           let test = 2 - index;
                           child.children[j].scale.y = test;
                       }
                    }
                }

        }
    })
}

/* Change position of the bones in the list */
function changePositionY(positionUpBones, positionDownBones, index){
    loadModel.traverse( child => {
        if (child.type == "Bone") {
                if ( positionUpBones.includes(child.name)) {
                    child.position.y = index;
                    let i = positionUpBones.indexOf(child.name);
                    positionUpBones.splice(i, 1);
                }

        }
    })
}

/* Get the information from the document and return index of actual scale*/
function calculateTransformation(id, range){
    let value = document.getElementById("a" + id).value;
    document.getElementById("b"  + id).innerText = value;
    let min = parseInt(document.getElementById("a"  + id).min);
    let max = parseInt(document.getElementById("a"  + id).max);
    let index = getScaleIndex(min, max, value, range);
    return index;
}

/* Get the information from the document and return index of actual position of Y*/
function calculateTranslationY(id, range, targetBone, originBoneList, originBonePositionY){
    let value = document.getElementById("a" + id).value;
    document.getElementById("b"  + id).innerText = value;
    let min = parseInt(document.getElementById("a"  + id).min);
    let max = parseInt(document.getElementById("a"  + id).max);
    let index = getPositionIndexY(min, max, value, range, targetBone, originBoneList, originBonePositionY);
    return index;
}


/* Calculate the actual scale index to transform the model*/
function getScaleIndex(min, max, value, range){
    //Ex: range = [0.85, 1.15] = 0.3
    let average = (min + max) / 2;
    let percentageIndex = (value - average) / (max - min);
    let actualIndex = percentageIndex * (range) + 1;
    return actualIndex;
}

/* Calculate the actual position index to transform the model*/
function getPositionIndexY(min, max, value, range, targetBone, originBoneList, originBonePositionY){
    let average = (min + max) / 2;
    let percentageIndex = (value - average) / (max - min);
    let targetBoneY = originBonePositionY[originBoneList.indexOf(targetBone)];
    let actualIndex = percentageIndex * (range) + targetBoneY;
    return actualIndex;
}

function loadOriginBones(modelBoneName, bonePositionY){
    loadModel.traverse( child => {
    if (child.type == "Bone") {
        if ( !modelBoneName.includes(child.name) && child.name.indexOf("J_Sec") == -1) {
            modelBoneName.push(child.name);
            bonePositionY.push(child.position.y);
            //console.log(child.name);
            //console.log(child.position.y);
        }
    }
})
}

/* change texture called by init function */
function textureChange(targetTextureName, newTexturePath) {
    loadModel.traverse( child => {
        if (child instanceof THREE.Mesh) {

            if (child.name.indexOf(targetTextureName) != -1) {

                var newTexture = new THREE.TextureLoader().load(newTexturePath);
                child.material.map = newTexture;
                child.material.needsUpdate = true;

            }
        }
    })
}

function readInput(input){
    input = input.split(",");
    for (let i = 0; i < input.length; i+=2) {
        textureChange(input[i], input[i+1]);
        //console.log(input[i], input[i+1]);
    }
}

//reference: http://zuoben.top/#4-10
// current1 相机当前的位置
// target1 相机的controls的target
// current2 新相机的目标位置
// target2 新的controls的target
var tween;
 
function animateCamera(current1, target1, current2, target2) {
    
    let positionVar = {
        x1: current1.x,
        y1: current1.y,
        z1: current1.z,
        x2: target1.x,
        y2: target1.y,
        z2: target1.z
    };
    
    controls.enabled = false;
    tween = new TWEEN.Tween(positionVar);
    tween.to({
        x1: current2.x,
        y1: current2.y,
        z1: current2.z,
        x2: target2.x,
        y2: target2.y,
        z2: target2.z
    }, 500);
    
    tween.onUpdate(function() {
        
        camera.position.x = positionVar.x1;
        camera.position.y = positionVar.y1;
        camera.position.z = positionVar.z1;
        controls.target.x = positionVar.x2;
        controls.target.y = positionVar.y2;
        controls.target.z = positionVar.z2;
        controls.update();
        
    })
 
    tween.onComplete(function() {
        controls.enabled = true;
    })
 
    tween.easing(TWEEN.Easing.Cubic.InOut);
    tween.start();
}
