var gulp = require('gulp');
var sass = require('gulp-sass')
var uglifycss = require('gulp-uglifycss');
var browserSync = require('browser-sync');
var exec = require('child_process').exec;

// gulp.task('sass', function () {
//     return gulp.src('./sass/*.sass')
//       .pipe(sass().on('error', sass.logError))
//       .pipe(gulp.dest('./css'));
//   });
//
//
//
gulp.task('css', function () {
    gulp.src('./web/static/libs/css/**/*.css')
      .pipe(uglifycss({

        "uglyComments": true
      }))
      .pipe(gulp.dest('./dist/'));
});




// gulp.task('run', done=>{
//     gulp.series('sass', 'css');
//     done();
// });



gulp.task('runserver', (done)=> {
    var proc = exec('python manager.py runserver');
    done();
});

gulp.task('run', done=>{
    gulp.series('css', 'runserver');
    done();
});

gulp.task('serve', gulp.series('run', function () {
    browserSync({
    // notify: false,
    proxy: "127.0.0.1:8999"
  });

    // gulp.watch('./sass/*.sass', gulp.series('sass'));
    gulp.watch('./web/static/libs/css/*/*.css', gulp.series('css'));
    gulp.watch('./web/templates/*/*.html').on('change', browserSync.reload);
    gulp.watch('./web/static/libs/css/**/*.css').on('change', browserSync.reload);


}));

// gulp.task('serve', gulp.series('run', function(){
//     browser_sync.init({
//         server: './'
//     });
//     gulp.watch('./sass/*.sass', gulp.series('sass'));
//     gulp.watch('./web/static/lib/*/*.css', gulp.series('css'));
//     gulp.watch('./web/templates/*/*.html').on('change', browser_sync.reload);
// }));







//gulp.task('watch', function(){
//    gulp.watch('./sass/*.sass', gulp.series('sass'));
//    gulp.watch('./css/*.css', gulp.series('css'));
//});

gulp.task('default', gulp.series('serve'));