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
        scene.background = new THREE.Color(0x000000);
        
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

//const loadmodel1;
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
            console.log(child.name);
            count += 1;
        }
    })
    console.log(count);
    console.log(vrm1)

    let group = scene.getObjectByName("Body");
    let hair = scene.getObjectByName("Hair");
    let face = scene.getObjectByName("Face");

    let bodySkin = scene.getObjectByName("Body_(merged)baked");
    let faceSkin = scene.getObjectByName("Face_(merged)(Clone)baked_3")
    //faceSkin.material = bodySkin.material;

    hair.children[0].visible = false;
    console.log(group.children);

    for (let i = 7; i < 14; i++) {
        face.children[i].visible = false;
    }

    for (let i = 0; i < 5; i++) {
        group.children[i].visible = false;
    }
    console.log(group.children);
    currentVrm = vrm1;

    animate();

}
init("/static/model/test/newtest.vrm")


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




