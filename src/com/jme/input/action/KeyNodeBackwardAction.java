/*
 * Copyright (c) 2003-2004, jMonkeyEngine - Mojo Monkey Coding
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer.
 *
 * Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * Neither the name of the Mojo Monkey Coding, jME, jMonkey Engine, nor the
 * names of its contributors may be used to endorse or promote products derived
 * from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 */
package com.jme.input.action;

import com.jme.math.Vector3f;
import com.jme.scene.Spatial;

/**
 * <code>KeyNodeBackwardAction</code> defines an action to move a
 * <code>Spatial</code> node along it's negative direction vector. The speed
 * of the node is defined by the speed and the value set in the
 * <code>performAction</code> method. The speed is set with construction or
 * the <code>setSpeed</code> method. This can be thought as units/second.
 * @author Mark Powell
 * @version $Id: KeyNodeBackwardAction.java,v 1.8 2004-05-08 02:48:27 renanse Exp $
 */
public class KeyNodeBackwardAction extends AbstractInputAction {
    private Spatial node;

    /**
     * Constructor creates a new <code>KeyNodeBackwardAction</code> object.
     * During construction, the node to direct and the speed at which to
     * move the node is set.
     * @param node the node that will be affected by this action.
     * @param speed the speed at which the camera can move.
     */
    public KeyNodeBackwardAction(Spatial node, float speed) {
        this.node = node;
        this.speed = speed;
    }

    /**
     * <code>performAction</code> moves the node along it's negative
     * direction vector at a speed of movement speed * time. Where time is
     * the time between frames and 1 corresponds to 1 second.
     * @see com.jme.input.action.InputAction#performAction(float)
     */
    public void performAction(float time) {
        Vector3f loc = node.getLocalTranslation();
        loc.subtractLocal(node.getLocalRotation().getRotationColumn(2).multLocal((speed*time)));
        node.setLocalTranslation(loc);
        node.updateWorldData(0);
    }
}
