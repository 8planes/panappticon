//
//  PanappticonSession.h
//  panappticon
//
//  Created by Adam Duston on 8/2/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>


@interface PanappticonSession : NSObject {
  NSString *_appName;
  NSString *_sessionID;
  NSDate *_sessionStart;
}

+ (PanappticonSession*)instance;

+ (void)start:(NSString*)appName;
+ (void)tag:(NSString*)tagName includeScreenshot:(BOOL)include;

@end
