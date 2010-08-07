//
//  PanappticonDatabase.h
//  Panappticon
//
//  Created by Adam Duston on 8/1/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

@interface PanappticonDatabase : NSObject {
  // can be accessed by any thread
  NSOperationQueue *_operationQueue;
  NSString *_appName;
  NSString *_sessionID;
  NSTimer *_cleanupTimer;
  NSString *_sessionFileDir;
  NSString *_sessionFile;
  NSString *_imageFileDir;
}

+ (PanappticonDatabase*)instance;

- (void)start:(NSString *)appName;
- (void)saveTag:(NSString*)tagName withScreenshot:(UIImage*)screenshot;
- (void)endSession;

@end
