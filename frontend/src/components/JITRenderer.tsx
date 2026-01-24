'use client'

import { CheckCircle, XCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

interface JITManifest {
  template: string;
  context: Record<string, string>;
}

export function JITRenderer({ 
  manifest, 
  onApprove, 
  onReject 
}: { 
  manifest: JITManifest, 
  onApprove: () => void, 
  onReject: () => void 
}) {
  const renderTemplate = () => {
    switch (manifest.template) {
      case 'high_value_confirm':
        return renderHighValueConfirm()
      default:
        return renderDefaultTemplate()
    }
  }

  const renderHighValueConfirm = () => {
    const context = manifest.context || {}
    
    return (
      <Card className="bg-card-bg border-2 border-cyberpunk-purple">
        <CardHeader>
          <CardTitle className="text-cyberpunk-purple">High Value Transaction Confirmation</CardTitle>
          <CardDescription>This transaction requires your explicit approval</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-300">Item:</span>
              <Badge variant="secondary" className="bg-gray-700">
                {context.item_name || 'Unknown Item'}
              </Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-300">Amount:</span>
              <Badge variant="secondary" className="bg-gray-700">
                ${context.price || 'N/A'}
              </Badge>
            </div>
            {context.item_id && (
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-300">Item ID:</span>
                <Badge variant="secondary" className="bg-gray-700">
                  {context.item_id}
                </Badge>
              </div>
            )}
          </div>
          <div className="p-3 bg-yellow-900/20 border border-yellow-700 rounded-md">
            <p className="text-sm text-yellow-400 font-medium">⚠️ Attention Required</p>
            <p className="text-xs text-gray-300 mt-1">
              This transaction exceeds the autonomous decision threshold and requires your explicit approval.
            </p>
          </div>
        </CardContent>
        <CardFooter className="flex justify-end space-x-3">
          <Button 
            variant="destructive" 
            onClick={onReject}
            className="bg-red-700 hover:bg-red-600"
          >
            <XCircle className="mr-2" size={16} />
            Reject
          </Button>
          <Button 
            onClick={onApprove}
            className="bg-green-700 hover:bg-green-600"
          >
            <CheckCircle className="mr-2" size={16} />
            Approve
          </Button>
        </CardFooter>
      </Card>
    )
  }

  const renderDefaultTemplate = () => {
    return (
      <Card className="bg-card-bg border border-gray-600">
        <CardHeader>
          <CardTitle className="text-cyberpunk-blue">Just-In-Time Decision</CardTitle>
          <CardDescription>Template: {manifest.template}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="p-3 bg-blue-900/20 border border-blue-700 rounded-md">
            <p className="text-sm text-blue-400">Context Data:</p>
            <pre className="text-xs text-gray-300 mt-2 overflow-x-auto">
              {JSON.stringify(manifest.context, null, 2)}
            </pre>
          </div>
        </CardContent>
        <CardFooter className="flex justify-end space-x-3">
          <Button variant="outline" onClick={onReject}>
            <XCircle className="mr-2" size={16} />
            Reject
          </Button>
          <Button onClick={onApprove}>
            <CheckCircle className="mr-2" size={16} />
            Approve
          </Button>
        </CardFooter>
      </Card>
    )
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="w-full max-w-2xl">
        {renderTemplate()}
      </div>
    </div>
  )
}