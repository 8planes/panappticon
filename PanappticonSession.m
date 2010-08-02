//
//  PanappticonSession.m
//  Panappticon
//
//  Created by Adam Duston on 8/1/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>

#import "PanappticonSession.h"
#import "PanappticonDatabase.h"
#import "Utilities.h"

static PanappticonSession *_instance = nil;

@interface PanappticonSession()

- (void)startImpl:(NSString*)appName;
- (void)tagImpl:(NSString*)tagName includeScreenshot:(BOOL)include;

@end

@implementation PanappticonSession

- (PanappticonSession*)init {
  if (self = [super init]) {
    self->_appName = nil;
    self->_sessionStart = nil;
    self->_sessionID = nil;
  }
  return self;
}

+ (PanappticonSession*)instance {
  @synchronized (self) {
    if (_instance == nil)
      _instance = [[self alloc] init];
  }
  return _instance;
}

+ (void)start:(NSString*)appName {
  [[PanappticonSession instance] startImpl:appName];
}

+ (void)tag:(NSString *)tagName includeScreenshot:(BOOL)include {
  [[PanappticonSession instance] tagImpl:tagName includeScreenshot:include];
}

#pragma mark -
#pragma mark Private Methods

- (void)startImpl:(NSString*)appName {
  @synchronized (self) {
    if (_appName != nil)
      @throw [NSException exceptionWithName:@"AlreadyStarted" 
                                     reason:@"Panappticon Session Already Started" 
                                   userInfo:nil];
    _appName = appName;
    _sessionID = [Utilities randomString];
    _sessionStart = [[NSDate alloc] init];
  }
  [PanappticonDatabase saveTag:@"SessionStarted" forApp:_appName 
                   forSession:_sessionID withScreenshot:nil];
}

- (void)tagImplWithImage:(NSString*)tagName withScreenshot:(UIImage*)screenshot {
  [PanappticonDatabase saveTag:tagName 
                       forApp:_appName 
                   forSession:_sessionID 
               withScreenshot:screenshot];
}

- (void)takeScreenshotAndTag:(NSString*)tagName {
  [self tagImplWithImage:tagName withScreenshot:[Utilities screenshot]];
}

- (void)tagImpl:(NSString*)tagName includeScreenshot:(BOOL)include {
  @synchronized (self) {
    if (_appName == nil)
      @throw [NSException exceptionWithName:@"NotStarted" 
                                     reason:@"Panappticon Session Not Started" 
                                   userInfo:nil];
  }
  if (!include)
    [self tagImplWithImage:tagName withScreenshot:nil];
  else {
    if ([NSThread isMainThread])
      [self takeScreenshotAndTag:tagName];
    else
      [self performSelectorOnMainThread:@selector(takeScreenshotAndTag:) 
                             withObject:tagName 
                          waitUntilDone:NO];
  }
}

@end
