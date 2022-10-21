import * as THREE from 'three';
import { FBXLoader } from '/static/js/FBXLoader.js';
import { GLTFLoader } from '/static/js/GLTFLoader.js';
import { OrbitControls } from '/static/js//OrbitControls.js';
import Stats from '/static/js/stats.module.js';
import { Scene } from '/static/js//three.module.js';
import * as dat from 'https://cdn.jsdelivr.net/npm/dat.gui@0.7.9/build/dat.gui.module.js';
import { Vector3 } from 'three';


let stats, mixer, canvas, canvasWidth, canvasHeight, clock;
let camera, scene, renderer, controls;
let loadModel,action;

let stats1, mixer1, canvas1, clock1;
let camera1, scene1, renderer1, controls1;
let loadModel1,action1;


let modelBoneName = [], bonePositionY = [];
var path = document.getElementById("model_path").innerText;
var hair_color = document.getElementById("hair_color").innerText;
var skin_color = document.getElementById("skin_color").innerText;
var top_dress = document.getElementById("top_dress").innerText;
var bottom_dress = document.getElementById("bottom_dress").innerText;

var basic_model_parameters_range = document.getElementById("basic_model_parameters_range").innerText;
basic_model_parameters_range = basic_model_parameters_range.replaceAll("(","");
basic_model_parameters_range = basic_model_parameters_range.replaceAll(")","");
basic_model_parameters_range = basic_model_parameters_range.split(",");
console.log(basic_model_parameters_range);

let latest_records = document.getElementById("latest_records").innerText;
latest_records = JSON.parse(latest_records);
console.log(latest_records);

var isOne = latest_records.length == 1;

var initPosition = 0.23;
//test version for model under /static/model/test2/ folder only
init("before_canvas");
init1("after_canvas");



function sceneInit(canvasID) {
        //canvas set up
        canvas = document.getElementById(canvasID);
        //document.body.appendChild(canvas);
        canvasWidth = document.getElementById(canvasID).clientWidth;
        canvasHeight = document.getElementById(canvasID).clientHeight;

        clock = new THREE.Clock();

        //set up camera
        camera = new THREE.PerspectiveCamera( 30, canvasWidth / canvasHeight, 0.1, 20);
        //camera.position.set(1.66,2.05,3.61);
        camera.position.set(1.4485807979862497,2.0668476949423362,3.934246459224377);
        //camera.rotation.set(-0.34, 0.51, 0.17);
        camera.lookAt(0,1,0);
        //console.log(camera);

        //scene set up, background color debug use only
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0xD6E7C5);
        
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
        // const gridHelper = new THREE.GridHelper(10, 10);
        // gridHelper.receiveShadow = true;
        // scene.add(gridHelper);

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

        controls.addEventListener( 'change', () => {
            camera1.position.copy( camera.position );
            camera1.rotation.copy( camera.rotation );
        } );
        //x=0.74,y=1.338,z=1.278 shang
        //x=0.7458 y = 0.69353, z=1.379
        
}   

async function init(canvasID) {

    // group = new THREE.Group();
    sceneInit(canvasID);



    //Async loader!
    const fbxLoader = new FBXLoader().setPath(path);
    [loadModel] = await Promise.all( [
        fbxLoader.loadAsync( 'Idle.fbx' )
    ] );

    // Read database store texture
    readInput(loadModel,hair_color);
    readInput(loadModel,skin_color);
    readInput(loadModel,top_dress);
    readInput(loadModel,bottom_dress);

    //Save the origin bones position data.
    loadOriginBones(modelBoneName, bonePositionY);

    loadModel.position.set(0,initPosition,0);
    loadingHistoryBodyData(loadModel,0);

    loadModel.traverse( child => {

        if (child instanceof THREE.Mesh) {
            child.material.transparent = true;
            child.material.side = THREE.DoubleSide;
            child.material.alphaTest = 0.5;
        }
    })

    scene.add(loadModel);

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
    scene.add(stage);

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
    //stats.update();
    
    //console.log(camera.position, controls.target);
    // console.log(camera.rotation)
    
}

function readInput(model,input){
    input = input.split(",");
    for (let i = 0; i < input.length; i+=2) {
        TextureChange(model,input[i], input[i+1]);
    }
}

function TextureChange(model,targetTextureName, newTexturePath) {
    model.traverse( child => {
        if (child instanceof THREE.Mesh) {

            if (child.name.indexOf(targetTextureName)!= -1) {

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
    //camera1.position.set(1.66,2.05,3.61);
    camera1.position.set(1.4485807979862497,2.0668476949423362,3.934246459224377);
    //camera.rotation.set(-0.34, 0.51, 0.17);
    camera1.lookAt(0,1,0);
    //console.log(camera);

    //scene set up, background color debug use only
    scene1 = new THREE.Scene();
    scene1.background = new THREE.Color(0xD6E7C5);
    
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
    // const gridHelper = new THREE.GridHelper(10, 10);
    // gridHelper.receiveShadow = true;
    // scene1.add(gridHelper);

    //set up stats
    //stats1 = new Stats();
    // document.body.appendChild( stats1.dom );

    //set up controller(enable user to control camera)
    controls1 = new OrbitControls(camera1, renderer1.domElement)
    controls1.enableDamping = true
    controls1.target.set(0, 1, 0)
    controls1.update()
    
    controls1.minPolarAngle = 0;
    controls1.maxPolarAngle =  Math.PI * 0.5;

    controls1.addEventListener( 'change', () => {
        camera.position.copy( camera1.position );
        camera.rotation.copy( camera1.rotation );
    } );
}

async function init1(canvasID, modelName) {

    // group = new THREE.Group();
    sceneInit1(canvasID);

    //Async loader!
    const fbxLoader = new FBXLoader().setPath(path);
    [loadModel1] = await Promise.all( [
        fbxLoader.loadAsync( 'Idle.fbx' )
    ] );

    readInput(loadModel1,hair_color);
    readInput(loadModel1,skin_color);
    readInput(loadModel1,top_dress);
    readInput(loadModel1,bottom_dress);

    loadModel1.position.set(0,initPosition,0);
     if(isOne){
        loadingHistoryBodyData(loadModel1,0);
        var canvas = document.getElementById("after_canvas");
        var before_canvas = document.getElementById("before_canvas");
        var text = document.getElementById("basic_stat")
        canvas.style.display = 'none';

        var after_canvas_text = document.getElementById("after_canvas_text");
        var before_canvas_text = document.getElementById("before_canvas_text");
        before_canvas_text.innerText = "Latest Model";
        after_canvas_text.style.display = 'none';
        text.style.float = "default";
        text.style.width = "500px";
        text.style.margin = "0px";
        text.style.marginLeft = "25px";
        
        text.style.padding = "10px";
        
    }
    else{
        loadingHistoryBodyData(loadModel1,1);
    }


    loadModel1.traverse( child => {

        if (child instanceof THREE.Mesh) {
            child.material.transparent = true;
            child.material.side = THREE.DoubleSide;
            child.material.alphaTest = 0.5;
        }
    })

    scene1.add(loadModel1);
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
    scene1.add(stage);

    scene1.traverse(child =>{
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
    TWEEN.update();
    requestAnimationFrame( animate1 );
    const delta = clock1.getDelta();
    if ( mixer1 ) mixer1.update( delta );
    renderer1.render( scene1, camera1 );

}

document.getElementById("Top").onclick = function cameraChange() {

    const cameraTarget = new Vector3(0.6248297296327294, 1.503963156706119, 1.3563233589083084)
    const controlTarget = new Vector3(-0.025193594935890188,
        1.133358866462773,
        0.012610338156221673)
    animateCamera(camera.position, controls.target,cameraTarget,controlTarget)

}

document.getElementById("Bottom").onclick = function cameraChange() {

    const cameraTarget = new Vector3(0.5902717381883454, 0.9486176075421906, 1.5785914227370572)
    const controlTarget = new Vector3(-0.046407628814892146,
        0.4610626823169693,
        -0.0650557742511241)
    animateCamera(camera.position, controls.target,cameraTarget,controlTarget)
}

document.getElementById("Top_side").onclick = function cameraChange() {

    const cameraTarget = new Vector3(1.308709997771635, 1.3521985284192815, -0.15307891073072163)
    const controlTarget = new Vector3(-0.004148981083599594,
        1.2025215018947184,
        -0.004882691356911102)
    animateCamera(camera.position, controls.target,cameraTarget,controlTarget)

}

document.getElementById("Bottom_side").onclick = function cameraChange() {

    const cameraTarget = new Vector3(1.3538168165687487, 0.7672824647324888, -0.27511724999154225)
    const controlTarget = new Vector3(0.07176819883779749,
        0.5801777022560607,
        0.023725818690882142)
    animateCamera(camera.position, controls.target,cameraTarget,controlTarget)

}

document.getElementById("Back").onclick = function cameraChange() {

    const cameraTarget = new Vector3(0.09798494493960556, 1.4677532125601949, -2.8010056092115954)
    const controlTarget = new Vector3(0.015196391403839911,
        0.8286177024522235,
        -0.004296867247283868)
    animateCamera(camera.position, controls.target,cameraTarget,controlTarget)

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
    }, 800);
    
    tween.onUpdate(function() {
        
        camera.position.x = positionVar.x1;
        camera.position.y = positionVar.y1;
        camera.position.z = positionVar.z1;
        controls.target.x = positionVar.x2;
        controls.target.y = positionVar.y2;
        controls.target.z = positionVar.z2;
        controls.update();
        
        console.log(positionVar);
    })
 
    tween.onComplete(function() {
        controls.enabled = true;
    })
 
    tween.easing(TWEEN.Easing.Cubic.InOut);
    tween.start();
}

/// 模型身体参数改变

//Method for changing the body due to parameter
function loadingHistoryBodyData(loadModel,model){
    changeHeightImpl(loadModel,model);
    changeWeightImpl(loadModel,model);
    changeThighImpl(loadModel,model);
    changeShankImpl(loadModel,model);
    changeHipImpl(loadModel,model);
    changeArmGrithImpl(loadModel,model);
    changeArmsPanImpl(loadModel,model);
    changeWaistImpl(loadModel,model);
    changeChestImpl(loadModel,model);
}

/* Get the information from the document and return index of actual scale*/
function calculateTransformation(model,id,part,range){
//    console.log(model,id,part);
    let value = parseFloat(latest_records[model][part]);
    let min = parseFloat(basic_model_parameters_range[id*2-1]);
    let max = parseFloat(basic_model_parameters_range[id*2]);
    let index = getScaleIndex(min, max, value, range);
//    console.log(value,min,max,index);
    return index;
}

/* Calculate the actual scale index to transform the model*/
function getScaleIndex(min, max, value, range){
    //Ex: range = [0.85, 1.15] = 0.3
    let average = (min + max) / 2;
    let percentageIndex = (value - average) / (max - min);
    let actualIndex = percentageIndex * (range) + 1;
//    console.log(average,percentageIndex,actualIndex);
    return actualIndex;
}

/* Get the information from the document and return index of actual position of Y*/
function calculateTranslationY(model,id,part, range, targetBone, originBoneList, originBonePositionY){
    let value = parseFloat(latest_records[model][part]);
    let min = parseFloat(basic_model_parameters_range[id*2-1]);
    let max = parseFloat(basic_model_parameters_range[id*2]);
    let index = getPositionIndexY(min, max, value, range, targetBone, originBoneList, originBonePositionY);
    return index;
}

/* Calculate the actual position index to transform the model*/
function getPositionIndexY(min, max, value, range, targetBone, originBoneList, originBonePositionY){
    let average = (min + max) / 2;
    let percentageIndex = (value - average) / (max - min);
    let targetBoneY = originBonePositionY[originBoneList.indexOf(targetBone)];
    let actualIndex = percentageIndex * (range) + targetBoneY;
    return actualIndex;
}


//API of modify bones
var callOnce = [0,0,0];
function changeHeightImpl(loadModel,model){
    let index = calculateTransformation(model,1,"height", 0.2);
    changeScaleX(loadModel,["Hips"], [], index);
    changeScaleY(loadModel,["Hips"], [], index);
    changeScaleZ(loadModel,["Hips"], [], index);

    //new stage/environment
    positionTranslate(loadModel,index);

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
function positionTranslate(loadModel,index) {
    loadModel.position.set(0,initPosition + (index-1),0);
}

function changeWeightImpl(loadModel,model){
    let index = calculateTransformation(model,2,"weight", 0.1);
    changeScaleX(loadModel,["Hips"], [], index);
    changeScaleZ(loadModel,["Hips"], [], index);
}

function changeChestImpl(loadModel,model){
    let index = calculateTransformation(model,3,"chest", 0.2);
    changeScaleZ(loadModel,["Upper_Chest"], ["Neck"], index);
}
function changeWaistImpl(loadModel,model){
    let path = document.getElementById("model_path").innerText;
    let index;
    if(path.indexOf("female") != -1){
        index = calculateTransformation(model,4,"waist", 0.3);
    }else{
        index = calculateTransformation(model,4,"waist", 0.2);
    }
    changeScaleX(loadModel,["Spine"], ["Chest"], index);
    changeScaleZ(loadModel,["Spine"], ["Chest"], index);
}


function changeHipImpl(loadModel,model){
    let index = calculateTransformation(model,5,"hip", 0.2);
    changeScaleZ(loadModel,["Hips"], ["Left_leg", "Right_leg", "Spine"], index);
}


function changeArmGrithImpl(loadModel,model){
    let index = calculateTransformation(model,6,"arm_girth", 0.4);
    changeScaleX(loadModel,["Left_arm", "Right_arm"], [], index);
    changeScaleZ(loadModel,["Left_arm", "Right_arm"], [], index);
}

function changeArmsPanImpl(loadModel,model){
    let index = calculateTranslationY(model,7,"arm_pan", 0.04, "Left_arm", modelBoneName, bonePositionY);
    changePositionY(loadModel,["Left_arm", "Right_arm"], [], index);
}

function changeThighImpl(loadModel,model){
    let index = calculateTransformation(model,8,"thigh", 0.3);
    changeScaleX(loadModel,["Left_leg", "Right_leg"], ["Left_knee", "Right_knee"], index);
    changeScaleZ(loadModel,["Left_leg", "Right_leg"], ["Left_knee", "Right_knee"], index);
}

function changeShankImpl(loadModel,model){
    let index = calculateTransformation(model,9,"shank", 0.3);
    changeScaleX(loadModel,["Left_knee", "Right_knee"], [], index);
    changeScaleZ(loadModel,["Left_knee", "Right_knee"], [], index);
}

/* Scale up and scale down the bones in the list */
function changeScaleX(loadModel,scaleUpBones, scaleDownBones, index){
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
function changeScaleZ(loadModel,scaleUpBones, scaleDownBones, index){
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
function changeScaleY(loadModel,scaleUpBones, scaleDownBones, index){
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
function changePositionY(loadModel,positionUpBones, positionDownBones, index){
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

//load origin bones data
function loadOriginBones(modelBoneName, bonePositionY){
    loadModel.traverse( child => {
    if (child.type == "Bone") {
        if ( !modelBoneName.includes(child.name) && child.name.indexOf("J_Sec") == -1) {
            modelBoneName.push(child.name);
            bonePositionY.push(child.position.y);
//            console.log(child.name);
//            console.log(child.position.y);
        }
    }
})
}



