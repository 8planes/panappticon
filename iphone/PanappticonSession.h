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
}

+ (PanappticonSession*)instance;

+ (void)start:(NSString*)appName withUploadURL:(NSURL*)url;
+ (void)tag:(NSString*)tagName includeScreenshot:(BOOL)include;

@end
