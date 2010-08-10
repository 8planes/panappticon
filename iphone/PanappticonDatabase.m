//
//  PanappticonDatabase.m
//  Panappticon
//
//  Created by Adam Duston on 8/1/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import "PanappticonDatabase.h"
#import "Utilities.h"
#import "UploadQueue.h"

#import <UIKit/UIKit.h>

static PanappticonDatabase *_instance = nil;

@interface PanappticonDatabase()

- (void)saveTagImpl:(NSArray*)args;
- (void)endSessionImpl:(NSNumber*)suspended;
- (void)ensurePathExists:(NSString*)path;
- (void)createSessionFile;
- (void)appendToSessionFile:(NSString*)tagName screenshotKey:(NSString*)screenshotKey;
- (void)appendStringToSessionFile:(NSString*)string;
- (void)saveAndSendImageFile:(UIImage*)screenshot withKey:(NSString*)screenshotKey;
- (void)cleanupNow;
- (void)cleanupNowImpl;

@end


@implementation PanappticonDatabase

- (PanappticonDatabase*)init {
  if (self = [super init]) {
    _appName = nil;
    _operationQueue = [[NSOperationQueue alloc] init];
    _operationQueue.maxConcurrentOperationCount = 1;
    NSString *docPath = 
      [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory,
                                           NSUserDomainMask, YES) 
       objectAtIndex:0];
    _sessionFileDir = [[docPath stringByAppendingPathComponent:@"panappticon/"] retain];
    _imageFileDir = [[docPath stringByAppendingPathComponent:@"panappticon/screenshots/"] retain];
  }
  return self;
}

+ (PanappticonDatabase*)instance {
  @synchronized (self) {
    if (!_instance)
      _instance = [[PanappticonDatabase alloc] init];
  }
  return _instance;
}

- (void)start:(NSString *)appName {
  @synchronized (self) {
    if (_appName != nil)
      @throw [NSException exceptionWithName:@"AlreadyStarted" 
                                     reason:@"Panappticon Database Already Started" 
                                   userInfo:nil];
    _appName = [appName retain];
    NSOperation *startOperation = [[NSInvocationOperation alloc]
                                   initWithTarget:self 
                                   selector:@selector(createSessionFile) 
                                   object:nil];
    [_operationQueue addOperation:startOperation];
    [startOperation release];
  }
  _cleanupTimer = 
    [[NSTimer scheduledTimerWithTimeInterval:60.0 
                            target:self 
                          selector:@selector(cleanupNow)
                          userInfo:nil 
                           repeats:YES] retain];
  [self cleanupNow];
}

- (void)saveTag:(NSString*)tagName withScreenshot:(UIImage*)screenshot {
  @synchronized (self) {
    if (_appName == nil) 
      @throw [NSException exceptionWithName:@"NotStarted" 
                                     reason:@"Panappticon Database Not Started" 
                                   userInfo:nil];
  }
  NSArray *args = [NSArray arrayWithObjects:tagName,  
                   (screenshot == nil ? 
                    (NSObject*)[NSNull null] : 
                    (NSObject*)screenshot), 
                   nil];
  NSOperation *operation = [[NSInvocationOperation alloc] 
                            initWithTarget:self 
                            selector:@selector(saveTagImpl:) 
                            object:args];
  [_operationQueue addOperation:operation];
  [operation release];
}

- (void)endSession:(BOOL)suspended {
  @synchronized (self) {
    if (_appName == nil) 
      @throw [NSException exceptionWithName:@"NotStarted" 
                                     reason:@"Panappticon Database Not Started" 
                                   userInfo:nil];
  }
  NSOperation *operation = [[NSInvocationOperation alloc]
                            initWithTarget:self selector:@selector(endSessionImpl:) 
                            object:[NSNumber numberWithBool:suspended]];
  [_operationQueue addOperation:operation];
  [operation release];
}

- (void)newSession {
  NSOperation *operation = [[NSInvocationOperation alloc]
                            initWithTarget:self selector:@selector(createSessionFile) 
                            object:nil];
  [_operationQueue addOperation:operation];
  [operation release];
  
}

- (void)dealloc {
  
  [super dealloc];
}

#pragma mark -
#pragma mark Private Methods

- (void)saveTagImpl:(NSArray*)args {
  NSString *tagName = [args objectAtIndex:0];
  NSObject *screenshotObj = [args objectAtIndex:1];
  UIImage *screenshot = nil;
  NSString * screenshotKey = @"";
  if (screenshotObj != [NSNull null]) {
    screenshot = (UIImage*)screenshotObj;
    screenshotKey = [Utilities randomString];
    [self saveAndSendImageFile:screenshot withKey:screenshotKey];
  }
  [self appendToSessionFile:tagName screenshotKey:screenshotKey];
}

- (void)ensurePathExists:(NSString*)path {
  NSFileManager *fileManager = [NSFileManager defaultManager];
  if (![fileManager fileExistsAtPath:path])
    [fileManager createDirectoryAtPath:path 
           withIntermediateDirectories:YES 
                            attributes:nil 
                                 error:NULL];
}

- (void)createSessionFile {
  _sessionID = [[Utilities randomString] retain];
  [self ensurePathExists:_sessionFileDir];
  [self ensurePathExists:_imageFileDir];
  _sessionFile = [[_sessionFileDir stringByAppendingPathComponent:
                  [NSString stringWithFormat:@"%@.txt", _sessionID]] retain];
  NSFileManager *fileManager = [NSFileManager defaultManager];
  NSData *blank = [[NSData alloc] init];
  [fileManager createFileAtPath:_sessionFile contents:blank attributes:nil];
  [blank release];
  [self appendStringToSessionFile:[NSString stringWithFormat:@"%@\n%@\n%@\n%@\n%@\n\n",
                                   [Utilities randomString], _appName, 
                                   [[UIDevice currentDevice] uniqueIdentifier],
                                   _sessionID, [NSDate date]]];
}

- (void)appendStringToSessionFile:(NSString*)string {
  NSFileHandle *sessionFile = [NSFileHandle fileHandleForWritingAtPath:_sessionFile];
  [sessionFile truncateFileAtOffset:[sessionFile seekToEndOfFile]];
  [sessionFile writeData:[string dataUsingEncoding:NSUTF8StringEncoding]];
  [sessionFile closeFile];
}

- (void)appendToSessionFile:(NSString*)tagName screenshotKey:(NSString*)screenshotKey {
  [self appendStringToSessionFile:[NSString stringWithFormat:@"%@\n%@\n%@\n\n",
                                   tagName, screenshotKey, [NSDate date]]];
}

- (void)saveAndSendImageFile:(UIImage*)screenshot withKey:(NSString*)screenshotKey {
  NSString *imageFileName = 
    [_imageFileDir stringByAppendingPathComponent:[NSString stringWithFormat:@"%@.png", screenshotKey]];
  NSData* imageData = UIImagePNGRepresentation(screenshot);
  NSFileManager *fileManager = [NSFileManager defaultManager];
  [fileManager createFileAtPath:imageFileName contents:imageData attributes:nil];
  [[UploadQueue instance] uploadFile:imageFileName withContentType:@"image/png"];
}

- (void)endSessionImpl:(NSNumber*)suspended {
  NSLog(@"Application suspended");
  if ([suspended boolValue])
    [self appendToSessionFile:@"Application Suspended" screenshotKey:@""];
  [[UploadQueue instance] uploadFile:_sessionFile withContentType:@"plain/text"];
}

- (void)cleanupNow {
  NSOperation *operation = [[NSInvocationOperation alloc]
                            initWithTarget:self selector:@selector(cleanupNowImpl) object:nil];
  [_operationQueue addOperation:operation];
  [operation release];
}

- (void)cleanupNowImpl {
  NSFileManager *fileManager = [NSFileManager defaultManager];
  NSArray *fileList = [fileManager contentsOfDirectoryAtPath:_sessionFileDir error:nil];
  NSString *fullFileName;
  for (NSString* file in fileList) {
    fullFileName = [_sessionFileDir stringByAppendingPathComponent:file];
    if (![fullFileName isEqualToString:_sessionFile] && ![file isEqualToString:@"screenshots"])
      [[UploadQueue instance] uploadFile:fullFileName withContentType:@"plain/text"];
  }
  fileList = [fileManager contentsOfDirectoryAtPath:_imageFileDir error:nil];
  for (NSString* file in fileList)
    [[UploadQueue instance] uploadFile:
     [_imageFileDir stringByAppendingPathComponent:file] 
                       withContentType:@"plain/png"];
}

@end
