/*
*    module
*/
var fmApp = angular.module('FMApp', ['ngRoute', 'ngResource']);

/*
*   FMCtrl controller
*/
function FMCtrl($scope, $http, MusicList, Music) {
    angular.element(document).ready(function() {
        analysisUrl();
        $('ul.thumb li').Zoomer({speedView:200,speedRemove:400,altAnim:true,speedTitle:400,debug:false});
    });

    //music player 
    $scope.index = 0;
    //locale key
    $scope.key = "52cac08c1d41c80eaec94c09";
    //doufm key
    // $scope.key = "52f8ca1d1d41c851663fcba7";
    $scope.current_channel = '华语';
    
    function playerInit(playReady, playEnded) {
        new jPlayerPlaylist({
            jPlayer: "#jquery_jplayer_1",
            cssSelectorAncestor: "#jp_container_1"
        }, 
        [],
        { 
            ready: playReady,
            ended: playEnded,
            swfPath: "/static/app/vender/jPlayer/js",
            supplied: "mp3",
            wmode: "window",
            smoothPlayBar: true,
            keyEnabled: true
        });
        $('#jp-share').html('<a href="#" data-toggle="tooltip" title="分享给好友!"><img src="/static/app/images/share1.png"></a>');
        
        $('#jp-share').zclip({
                path: '/static/app/vender/ZeroClipboard.swf',
                copy: function(){
                    return $scope.shareMsg.replace(/\<br \/\>/g, '\r\n');
                },
                afterCopy: function (){
                    $('#share').modal('hide');
                }
            });
    }

    function playReady() {
        // console.info(" playReady ok");
        MusicList.query(function(data) {
            // console.info(data);
            // $scope.key = data[0].key;
            $scope.musics = MusicList.query({arg: $scope.key, num: 10}, function(data) {
                playMusic(data[$scope.index]);
            });
        });
    };

    function playEnded() {
        // console.info('playEnded ok');
        $scope.index = $scope.index + 1;
        console.info($scope.index);
        if($scope.index == 10) {
            $scope.index = 0;
            playReady();
        } else {
            console.info('playMusic');
            playMusic($scope.musics[$scope.index]);
        }
    };

    function playMusic(musicArr){
        // console.info(musicArr);
        var currentUrl = window.location.host;
        // console.log(currentUrl);
        $scope.shareMsg = '很好听的一首歌，快来听吧!<br />' + musicArr.artist + '--' + musicArr.title + "<br />http://" + currentUrl + '/#key=' + musicArr.key ;
        $('#shareMsg').html($scope.shareMsg);
        $("#jquery_jplayer_1").jPlayer("setMedia", { mp3: musicArr.audio }).jPlayer("load").jPlayer("play");
        $("#jp-cover img").attr("src",musicArr.cover);
        $("#jp-singer").html(musicArr.artist);
        $("#nameAlbum").html(musicArr.title + '     ' + musicArr.album);
    }

    function analysisUrl () {
        var url = window.location.href;
        // console.log(url);
        var shareKey = url.split('=')[1];
        if(shareKey != null) {
            playerInit(shareReady(shareKey), shareEnded);
        } else {
            playerInit(playReady, playEnded);
            // console.log(url);
        }
    }

    //share ready
    var shareReady = function (shareKey) {
        console.log(shareKey);
        Music.query({key: shareKey}, function(data) {
            console.log(data);
            playMusic(data[0]);
            $('#recentTenSongs').css('display', 'none');
        });
    }

    //share ended
    function shareEnded () {
        $('#shareEnd').modal('show');
    }

    //click next button in the music player
    $scope.clickNext = function() {
        $scope.index = $scope.index + 1;
        // console.info($scope.index);
        if($scope.index == 10) {
            $scope.index = 0;
            playReady();
        } else {
            // console.info('playMusic');
            playMusic($scope.musics[$scope.index]);
        }
    }

    //click cover in the recent 10 musics
    $scope.clickPlay = function(index) {
        // console.info(index);
        $scope.index = index;
        playMusic($scope.musics[index]);
    }

    //list for all users 
    $scope.lists = MusicList.query({start: 0});
    $scope.playthis = function(key, name) {
        // var listKey = key;
        $scope.key = key;
        $scope.current_channel = name;
        $scope.index = 0;
        $scope.musics = MusicList.query({arg: $scope.key, num: 10}, function(data) {
            playMusic(data[0]);
        });
    }
}

/*
*   manager controller
*/
function managerCtrl($scope, $http, Music, Channel, User) {
    
    //music info display
    $scope.musics = Music.query({start: 0, end: 14});

    // channel info display
    $scope.channelNumAll = Channel.get();
    $scope.channels = Channel.query({start: 0, end: 14});

    //user info display
    $scope.users = User.query({start: 0});
}

/*
*   personal controller
*/
function personalCtrl($scope, $http, Music, User) {
    $scope.currentUser = User.get({arg: 'current/'});
}