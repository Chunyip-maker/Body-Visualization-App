let currentAnimationUrl = "/static/model/test2/Breathing Idle (9).fbx";
const clock = new THREE.Clock();
let stats, mixer, canvas, canvasWidth, canvasHeight, currentMixer, currentVrm;
let camera, scene, renderer, controls, group;
let action;

function sceneInit(canvasID) {
        //canvas set up
        canvas = document.getElementById(canvasID);
        canvasWidth = document.getElementById(canvasID).clientWidth;
        canvasHeight = document.getElementById(canvasID).clientHeight;

        //set up camera
        camera = new THREE.PerspectiveCamera( 30, canvasWidth / canvasHeight, 0.1, 20);
        camera.position.set(1.66,2.05,3.61);
        camera.lookAt(0,1,0);
        //console.log(camera);

        //scene set up, background color debug use only
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0xf2f2f2);
        
        //set up render
        renderer = new THREE.WebGLRenderer();
        renderer.setSize( canvasWidth , canvasHeight );
        renderer.setPixelRatio( window.devicePixelRatio );
        renderer.outputEncoding = THREE.sRGBEncoding;

        document.body.appendChild( renderer.domElement );
     
        canvas.appendChild(renderer.domElement);

        //light
        const light = new THREE.DirectionalLight( 0xffffff );
        light.position.set( 1.0, 1.0, 1.0 ).normalize();
        scene.add( light );

        //grid
        const gridHelper = new THREE.GridHelper(10, 10);
        gridHelper.receiveShadow = true;
        scene.add(gridHelper);

        //set up controller(enable user to control camera)
        controls = new THREE.OrbitControls( camera, renderer.domElement );
        controls.enableDamping = true
        controls.target.set(0, 1, 0)
        controls.update()
}


let loadModel, tempModel;
async function init(modelUrl) {

    sceneInit("canvas");
    const loader = new THREE.GLTFLoader();

    loader.register((parser) => {return new THREE_VRM.VRMLoaderPlugin( parser, {autoUpdateHumanBones: true } );}); // here we are installing VRMLoaderPlugin
    [loadModel, tempModel] = await Promise.all(
        [
            loader.loadAsync("/static/model/test2/test9.vrm"),
            loader.loadAsync("/static/model/test2/newVrm.vrm")
        ]
    )
    
    //console.log(loadModel);
    const vrm1= loadModel.userData.vrm
    const vrm2= tempModel.userData.vrm
    scene.add(vrm1.scene);

    scene.traverse(child =>{
        if (child instanceof THREE.Mesh) {
            child.frustumCulled = false;
        }
    })

    var gui = new dat.GUI();
    let count = 0;
    scene.traverse(child =>{
        if (child.type == "Bone") {
             gui.add(child.scale, "x",0,2).name(child.name + "x");
             gui.add(child.scale, "y",0,2).name(child.name + "y");
             gui.add(child.scale, "z",0,2).name(child.name + "z");
            //console.log(child.name);
            count += 1;
        }
    })
    //console.log(count);
    console.log(vrm1)

    let group = scene.getObjectByName("Body");
    let hair = scene.getObjectByName("Hair");
    let face = scene.getObjectByName("Face");

    let bodySkin = scene.getObjectByName("Body_(merged)baked");
    let faceSkin = scene.getObjectByName("Face_(merged)(Clone)baked_3")
    console.log(hair.children[1].material.uniforms)


    
    //faceSkin.material = bodySkin.material;

    hair.children[0].visible = false;
    //console.log(hair.children[1]);

    for (let i = 7; i < 14; i++) {
        face.children[i].visible = false;
    }

    //attribute to change MtoonMaterial color
    //litfactor, shadeColorFactor

    for (let i = 5; i < group.children.length; i++) {
        group.children[i].visible = false;
    }

    console.log(group.children);
    currentVrm = vrm1;

    loadFBX( currentAnimationUrl );
    animate();

}
init("/static/model/test/newtest.vrm")

//loadVRM( defaultModelUrl );
// www.beian.gov.cn/portal/index?login=Y&token=22ba3e0f-dcba-4799-9c97-d4fccd4732c1&info=%E6%B3%A8%E5%86%8C%E6%88%90%E5%8A%9F%EF%BC%81
// mixamo animation
function loadFBX( animationUrl ) {
    currentAnimationUrl = animationUrl;
    // create AnimationMixer for VRM
    currentMixer = new THREE.AnimationMixer( currentVrm.scene );
    // Load animation
    loadMixamoAnimation( animationUrl, currentVrm ).then( ( clip ) => {
        // Apply the loaded animation to mixer and play
        currentMixer.clipAction( clip ).play();
    } );

}

// animate

function animate() {
    //console.log(1);
    requestAnimationFrame( animate );
    const deltaTime = clock.getDelta();
    // if animation is loaded
    if ( currentMixer ) {
        currentMixer.update( deltaTime );
    }
    if ( currentVrm ) {
        currentVrm.update( deltaTime );
    }
    renderer.render( scene, camera );
}





